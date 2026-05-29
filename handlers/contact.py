"""
Telefon raqam qabul qilish va buyurtmani yakunlash.
4-bosqich: to'liq ishlab tekshirilgan versiya.
"""

import re
import logging
from datetime import datetime, timezone, timedelta

from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

import config
from keyboards import remove_keyboard, phone_keyboard
from states import RegistrationStates
from services.sheets import save_to_sheets
from services.notifier import notify_admin

logger = logging.getLogger(__name__)
router = Router(name="contact")

# +998XXXXXXXXX — 9 ta raqam
PHONE_RE = re.compile(r"^\+998\d{9}$")

# ─── O'zbekiston vaqt zonasi UTC+5 ────────────────────────────────────────────
_UZ_TZ = timezone(timedelta(hours=5))


def _normalize_phone(raw: str) -> str:
    """Raqamdan bo'sh joy va tirelani olib tashlaydi."""
    return re.sub(r"[\s\-().]", "", raw)


# ─── 1. Contact tugma orqali ──────────────────────────────────────────────────

@router.message(RegistrationStates.waiting_phone, F.contact)
async def process_contact(message: Message, state: FSMContext) -> None:
    """Foydalanuvchi «Raqamni yuborish» tugmasini bosganida."""
    phone = message.contact.phone_number
    if not phone.startswith("+"):
        phone = "+" + phone
    phone = _normalize_phone(phone)

    await _finish_registration(message, state, phone)


# ─── 2. Qo'lda matn orqali ────────────────────────────────────────────────────

@router.message(RegistrationStates.waiting_phone, F.text)
async def process_phone_text(message: Message, state: FSMContext) -> None:
    """Foydalanuvchi telefon raqamini qo'lda kiritganida."""
    phone = _normalize_phone(message.text.strip())

    if not PHONE_RE.match(phone):
        await message.answer(
            text=config.MESSAGES["invalid_phone"],
            reply_markup=remove_keyboard(),
        )
        await message.answer(
            text="👇 Tugmani bosing yoki +998XXXXXXXXX formatda kiriting:",
            reply_markup=phone_keyboard(),
        )
        return

    await _finish_registration(message, state, phone)


# ─── Umumiy yakunlash funksiyasi ──────────────────────────────────────────────

async def _finish_registration(
    message: Message,
    state: FSMContext,
    phone: str,
) -> None:
    """
    Barcha ma'lumotlarni yig'ib:
    1. Google Sheets ga saqlaydi
    2. Admin kanalga xabar yuboradi
    3. Foydalanuvchiga muvaffaqiyat yoki xato xabari ko'rsatadi
    4. Holatni tozalaydi
    """
    data = await state.get_data()
    user = message.from_user

    now_uz = datetime.now(tz=_UZ_TZ)
    sana = now_uz.strftime("%d.%m.%Y %H:%M")

    order = {
        "name":     data.get("name", ""),
        "region":   data.get("region", ""),
        "quantity": data.get("quantity", ""),
        "phone":    phone,
        "user_id":  user.id,
        "username": user.username or "—",
        "date":     sana,
    }

    # ── 1. Google Sheets ga saqlash ───────────────────────────────────────────
    sheets_ok = False
    try:
        sheets_ok = await save_to_sheets(order)
    except Exception as exc:
        logger.error("save_to_sheets kutilmagan xato: %s", exc, exc_info=True)

    # ── 2. Admin kanalga xabar yuborish ───────────────────────────────────────
    notify_ok = False
    try:
        bot: Bot = message.bot
        notify_ok = await notify_admin(bot, order)
    except Exception as exc:
        logger.error("notify_admin kutilmagan xato: %s", exc, exc_info=True)

    # ── 3. Foydalanuvchiga javob ──────────────────────────────────────────────
    summary = (
        f"📋 <b>Buyurtma ma'lumotlari:</b>\n\n"
        f"👤 Ism: {order['name']}\n"
        f"🌍 Viloyat: {order['region']}\n"
        f"🌱 Ko'chat soni: {order['quantity']}\n"
        f"📞 Telefon: {order['phone']}\n"
        f"🕐 Vaqt: {order['date']}"
    )
    await message.answer(text=summary, reply_markup=remove_keyboard())

    if not sheets_ok and not notify_ok:
        await message.answer(text=config.MESSAGES["service_error"])
        logger.warning(
            "Ikkala servis ham ishlamadi! user_id=%s phone=%s",
            order["user_id"],
            order["phone"],
        )
    else:
        await message.answer(text=config.MESSAGES["success"])

        if not sheets_ok:
            logger.warning(
                "Google Sheets ishlamadi, lekin admin xabari yuborildi. user_id=%s",
                order["user_id"],
            )
        if not notify_ok:
            logger.warning(
                "Admin xabari yuborilmadi, lekin Sheets ga saqlandi. user_id=%s",
                order["user_id"],
            )

    # ── 4. Holatni tozalash ───────────────────────────────────────────────────
    await state.clear()

    logger.info(
        "Buyurtma yakunlandi: user_id=%s | region=%s | phone=%s | sheets=%s | notify=%s",
        order["user_id"],
        order["region"],
        order["phone"],
        "✓" if sheets_ok else "✗",
        "✓" if notify_ok else "✗",
    )
