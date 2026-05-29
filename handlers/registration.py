from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

import config
from keyboards import region_keyboard, quantity_keyboard, phone_keyboard
from states import RegistrationStates

router = Router(name="registration")


# ─── 1. Ism qabul qilish ───────────────────────────────────────────────────────

@router.message(RegistrationStates.waiting_name)
async def process_name(message: Message, state: FSMContext) -> None:
    """
    Foydalanuvchi ismini qabul qiladi.
    Kamida 2 ta harf bo'lishi shart; bo'sh yoki juda qisqa bo'lsa qayta so'raladi.
    """
    name = (message.text or "").strip()

    if len(name) < 2 or not any(ch.isalpha() for ch in name):
        await message.answer(text=config.MESSAGES["invalid_name"])
        return

    await state.update_data(name=name)
    await message.answer(
        text=config.MESSAGES["ask_region"],
        reply_markup=region_keyboard(),
    )
    await state.set_state(RegistrationStates.waiting_region)


# ─── 2. Viloyat qabul qilish ───────────────────────────────────────────────────

@router.message(RegistrationStates.waiting_region, F.text.in_(config.REGIONS))
async def process_region(message: Message, state: FSMContext) -> None:
    """Ro'yxatdagi viloyatni qabul qiladi va ko'chat miqdorini so'raydi."""
    await state.update_data(region=message.text)
    await message.answer(
        text=config.MESSAGES["ask_quantity"],
        reply_markup=quantity_keyboard(),
    )
    await state.set_state(RegistrationStates.waiting_quantity)


@router.message(RegistrationStates.waiting_region)
async def process_region_invalid(message: Message, state: FSMContext) -> None:
    """Ro'yxatdan tashqari viloyat kiritilsa qayta so'raladi."""
    await message.answer(
        text="⚠️ Iltimos, quyidagi ro'yxatdan viloyatni tanlang:",
        reply_markup=region_keyboard(),
    )


# ─── 3. Ko'chat miqdori qabul qilish ──────────────────────────────────────────

@router.message(
    RegistrationStates.waiting_quantity,
    F.text.in_(config.SEEDLING_QUANTITIES),
)
async def process_quantity(message: Message, state: FSMContext) -> None:
    """Ro'yxatdagi miqdorni qabul qiladi va telefon raqam so'raydi."""
    await state.update_data(quantity=message.text)
    await message.answer(
        text=config.MESSAGES["ask_phone"],
        reply_markup=phone_keyboard(),
    )
    await state.set_state(RegistrationStates.waiting_phone)


@router.message(RegistrationStates.waiting_quantity)
async def process_quantity_invalid(message: Message, state: FSMContext) -> None:
    """Ro'yxatdan tashqari miqdor kiritilsa qayta so'raladi."""
    await message.answer(
        text="⚠️ Iltimos, quyidagi variantlardan birini tanlang:",
        reply_markup=quantity_keyboard(),
    )
