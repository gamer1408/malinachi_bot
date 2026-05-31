from aiogram import Router, types  # types ni import qilganmiz
from aiogram.types import Message  # Mana bu qator yetishmayapti
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import re
import config
from services.sheets import save_to_sheets

router = Router()

class AdminOrder(StatesGroup):
    waiting_for_text = State()

@router.message(Command("clients")) 
async def start_client_order(message: Message, state: FSMContext):
    if message.from_user.id != int(config.ADMIN_ID):
        return

    await message.answer("Admin tasdiqlandi. Iltimos, mijoz ma'lumotlarini yuboring:")
    await state.set_state(AdminOrder.waiting_for_text)

@router.message(AdminOrder.waiting_for_text)
async def process_text(message: types.Message, state: FSMContext):
    text = message.text
    
    # Ma'lumotlarni regex orqali ajratib olish
    patterns = {
        'ism': r"(?:Ism|Nomi|Mijoz):\s*(.*)",
        'viloyat': r"(?:Viloyat|Manzil):\s*(.*)",
        'kochat': r"(?:Ko'chat|Soni|Tup):\s*(\d+)",
        'telefon': r"(\+?\d[\d\s-]{7,})"
    }
    
    extracted = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            # Telefon uchun butun qatorni, qolganlari uchun gruppani olamiz
            extracted[key] = match.group(0).strip() if key == 'telefon' else match.group(1).strip()
    
    # Telefon majburiy
    if 'telefon' not in extracted:
        await message.answer("❌ Xatolik: Xabarda kamida telefon raqam topilishi shart! Iltimos, qaytadan urinib ko'ring.")
        return

    # O'zgaruvchilarni tayyorlash
    ism = extracted.get('ism', "Noma'lum")
    viloyat = extracted.get('viloyat', "Noma'lum")
    kochat = extracted.get('kochat', "0")
    tel = extracted['telefon']
    
    # 1. Kanallga chiroyli formatda jo'natish
    channel_text = (f"🔔 <b>Yangi Buyurtma</b>\n\n"
                    f"👤 Ism: {ism}\n"
                    f"📍 Viloyat: {viloyat}\n"
                    f"🌱 Ko'chat: {kochat} tup\n"
                    f"📞 Telefon: {tel}")
    
    await message.bot.send_message(config.ADMIN_CHANNEL_ID, channel_text)
    
    # 2. Sheets ga saqlash uchun lug'at tuzish
    data_to_save = {
        "user_id": message.from_user.id,
        "username": message.from_user.username or "—",
        "name": ism,
        "region": viloyat,
        "quantity": kochat,
        "phone": tel
    }
    
    success = await save_to_sheets(data_to_save)
    
    if success:
        await message.answer("✅ Mijoz ma'lumotlari kanalga va bazaga saqlandi!")
    else:
        await message.answer("⚠️ Mijoz kanalga yuborildi, lekin bazaga saqlashda xatolik yuz berdi!")
    
    await state.clear()