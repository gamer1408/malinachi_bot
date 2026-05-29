"""
Admin kanalga xabar yuborish — 4-bosqich.

ADMIN_CHANNEL_ID da bot admin bo'lishi shart.
Kanal ID ni topish: pastdagi yo'riqnomaga qarang (main.py dagi on_startup logi).
"""

import logging
from datetime import datetime, timezone, timedelta

from aiogram import Bot
from aiogram.exceptions import TelegramAPIError

import config

logger = logging.getLogger(__name__)

_UZ_TZ = timezone(timedelta(hours=5))


def _format_admin_message(user_data: dict) -> str:
    """Admin kanalga yuboriladigan HTML xabar matnini tayyorlaydi."""
    now_uz = datetime.now(tz=_UZ_TZ)
    sana = now_uz.strftime("%d.%m.%Y %H:%M")

    name     = user_data.get("name", "—")
    region   = user_data.get("region", "—")
    quantity = user_data.get("quantity", "—")
    phone    = user_data.get("phone", "—")
    user_id  = user_data.get("user_id", "—")
    username = user_data.get("username", "—")

    if username and username != "—":
        tg_link = f'<a href="tg://user?id={user_id}">@{username}</a>'
    else:
        tg_link = f'<a href="tg://user?id={user_id}">ID: {user_id}</a>'

    message = (
        "🆕 <b>YANGI BUYURTMA!</b>\n"
        "━━━━━━━━━━━━━━━\n"
        f"👤 Ism: <b>{name}</b>\n"
        f"📍 Viloyat: {region}\n"
        f"🌱 Ko'chat soni: {quantity}\n"
        f"📞 Telefon: <code>{phone}</code>\n"
        f"🔗 Telegram: {tg_link}\n"
        f"🆔 ID: <code>{user_id}</code>\n"
        f"🕐 Vaqt: {sana}\n"
        "━━━━━━━━━━━━━━━\n"
        "#yangi_lead #malinachi"
    )

    return message


async def notify_admin(bot: Bot, user_data: dict) -> bool:
    """
    Yangi buyurtma haqida admin kanalga xabar yuboradi.

    Parametrlar:
        bot       (Bot):  Aiogram Bot obyekti
        user_data (dict): Buyurtma ma'lumotlari

    Qaytaradi:
        bool: Yuborildi — True, xato — False
    """
    try:
        text = _format_admin_message(user_data)

        await bot.send_message(
            chat_id=config.ADMIN_CHANNEL_ID,
            text=text,
            parse_mode="HTML",
            disable_web_page_preview=True,
        )

        logger.info(
            "Admin kanalga xabar yuborildi: %s | %s | %s",
            user_data.get("name"),
            user_data.get("region"),
            user_data.get("phone"),
        )
        return True

    except TelegramAPIError as tg_err:
        logger.error(
            "Telegram API xatosi (admin kanal=%s): %s",
            config.ADMIN_CHANNEL_ID,
            tg_err,
        )
        return False

    except Exception as exc:
        logger.error("notify_admin kutilmagan xato: %s", exc, exc_info=True)
        return False
