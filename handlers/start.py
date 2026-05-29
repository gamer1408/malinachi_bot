from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

import config
from keyboards import remove_keyboard
from states import RegistrationStates

router = Router(name="start")


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    """
    /start komandasi:
    1. Mavjud holatni tozalash (qayta boshlash uchun)
    2. Xush kelibsiz xabari
    3. Ism so'rash → waiting_name holatiga o'tish
    """
    await state.clear()

    await message.answer(
        text=config.MESSAGES["welcome"],
        reply_markup=remove_keyboard(),
    )
    await message.answer(text=config.MESSAGES["ask_name"])
    await state.set_state(RegistrationStates.waiting_name)
