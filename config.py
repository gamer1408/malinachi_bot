import os
from dotenv import load_dotenv

load_dotenv()

# ─── Bot asosiy sozlamalari ────────────────────────────────────────────────────
BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
ADMIN_CHANNEL_ID: int = int(os.getenv("ADMIN_CHANNEL_ID", "-1001234567890"))

# ─── Google Sheets sozlamalari ─────────────────────────────────────────────────
GOOGLE_SHEET_ID: str = os.getenv("GOOGLE_SHEET_ID", "")

# MUHIM O'ZGARISH: Fayl qidirish o'rniga Railway o'zgaruvchisini olamiz
GOOGLE_CREDENTIALS: str = os.getenv("GOOGLE_CREDENTIALS", "")

# ─── Viloyatlar ro'yxati (14 viloyat + Qoraqalpog'iston) ──────────────────────
REGIONS: list[str] = [
    "Toshkent sh.",
    "Toshkent vil.",
    "Andijon",
    "Farg'ona",
    "Namangan",
    "Samarqand",
    "Buxoro",
    "Navoiy",
    "Qashqadaryo",
    "Surxondaryo",
    "Sirdaryo",
    "Jizzax",
    "Xorazm",
    "Qoraqalpog'iston",
]

# ─── Ko'chat soni variantlari ──────────────────────────────────────────────────
SEEDLING_QUANTITIES: list[str] = [
    "10-50",
    "50-100",
    "100-500",
    "500+",
]

# ─── Google Sheets ustun nomlari ───────────────────────────────────────────────
SHEET_COLUMNS: list[str] = [
    "№",
    "Sana va vaqt",
    "Telegram ID",
    "Username",
    "Ism",
    "Viloyat",
    "Ko'chat soni",
    "Telefon raqam",
    "Holat",
]

# ─── Holat konstantalari ───────────────────────────────────────────────────────
class OrderStatus:
    NEW      = "Yangi lead 🟢"
    CALLED   = "Qo'ng'iroq qilindi"
    DONE     = "Bajarildi"
    REJECTED = "Rad etildi"
    

# ─── Bot xabarlari (o'zbek tilida) ─────────────────────────────────────────────
MESSAGES: dict[str, str] = {
    "welcome": (
        "Assalomu alaykum! Malinachi_ ga xush kelibsiz! 🍓\n"
        "Ko'chat oldindan buyurtma qilish uchun quyidagi savollarga javob bering."
    ),
    "ask_name": "👤Ismingizni kiriting:",
    "ask_region": "🌍Qaysi viloyatdansiz? (Quyidagi tugmalardan tanlang)",
    "ask_quantity": "🌱Taxminan nechta ko'chat kerak bo'ladi?",
    "ask_phone": "📞Telefon raqamingizni yuboring:",
    "success": (
        "✅ Rahmat! Sizning buyurtmangiz qabul qilindi.\n"
        "Tez orada menejer siz bilan bog'lanadi!\n"
        "Kanalimizga obuna bo'ling: @malinach_i"
    ),
    "error": "❌ Xatolik yuz berdi. Iltimos qaytadan urinib ko'ring.",
    "service_error": (
        "⚠️ Buyurtmangiz qabul qilindi, lekin texnik muammo sababli\n"
        "ma'lumotlarni saqlashda xatolik yuz berdi.\n"
        "Iltimos, bevosita bog'laning: @malinachi_admin"
    ),
    "invalid_name": (
        "⚠️ Iltimos, to'g'ri ism kiriting (kamida 2 ta harf)."
    ),
    "invalid_phone": (
        "⚠️ Telefon raqami noto'g'ri. Iltimos, «Raqamni yuborish» tugmasini "
        "bosing yoki qo'lda kiriting: +998XXXXXXXXX"
    ),
    "cancel": "🚫 Buyurtma bekor qilindi. Qaytadan boshlash uchun /start yozing.",
    "admin_new_order": (
        "📥 <b>Yangi buyurtma!</b>\n\n"
        "👤 Ism: {name}\n"
        "🌍 Viloyat: {region}\n"
        "🌱 Ko'chat soni: {quantity}\n"
        "📞 Telefon: {phone}\n"
        "🔗 Telegram: @{username}\n"
        "🆔 ID: <code>{user_id}</code>\n"
        "📅 Sana: {date}"
    ),
}

# ─── Tekshirish ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    missing = []
    if not BOT_TOKEN:
        missing.append("BOT_TOKEN")
    if not GOOGLE_SHEET_ID:
        missing.append("GOOGLE_SHEET_ID")
    if not GOOGLE_CREDENTIALS:
        missing.append("GOOGLE_CREDENTIALS")
    if missing:
        print(f"[!] Muhit o'zgaruvchilari to'ldirilmagan: {', '.join(missing)}")
    else:
        print("[✓] Barcha muhit o'zgaruvchilari to'g'ri sozlangan.")