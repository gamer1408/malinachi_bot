from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove,
)

import config


def region_keyboard() -> ReplyKeyboardMarkup:
    """config.REGIONS dan viloyatlar klaviaturasi."""
    buttons = [
        [KeyboardButton(text=region)]
        for region in config.REGIONS
    ]
    return ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Viloyatni tanlang...",
    )


def quantity_keyboard() -> ReplyKeyboardMarkup:
    """config.SEEDLING_QUANTITIES dan ko'chat miqdori klaviaturasi."""
    quantities = config.SEEDLING_QUANTITIES
    buttons = []
    for i in range(0, len(quantities), 2):
        row = [KeyboardButton(text=quantities[i])]
        if i + 1 < len(quantities):
            row.append(KeyboardButton(text=quantities[i + 1]))
        buttons.append(row)
    return ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Miqdorni tanlang...",
    )


def phone_keyboard() -> ReplyKeyboardMarkup:
    """Kontakt yuborish tugmasi."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📱 Raqamni yuborish", request_contact=True)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def remove_keyboard() -> ReplyKeyboardRemove:
    """Klaviaturani olib tashlash."""
    return ReplyKeyboardRemove()
