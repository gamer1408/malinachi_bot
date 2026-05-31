"""
Malinachi.uz Telegram Bot
=========================
4-bosqich: To'liq ishlaydigan, Docker-tayyor versiya.
"""

import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

import config
from handlers.start import router as start_router
from handlers.registration import router as registration_router
from handlers.contact import router as contact_router
from services.sheets import check_sheets_connection
from handlers.admin import router as admin_router # Tepaga qo'sh


# ─── Logging ───────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s — %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


# ─── Muhit o'zgaruvchilarini tekshirish (startup dan oldin) ───────────────────
def _check_env() -> None:
    errors = []

    if not config.BOT_TOKEN:
        errors.append("  ❌ BOT_TOKEN — bo'sh! (@BotFather dan oling)")

    if config.ADMIN_CHANNEL_ID == -1001234567890:
        errors.append("  ⚠️  ADMIN_CHANNEL_ID — default qiymat! Haqiqiy kanal ID ni kiriting")

    if not config.GOOGLE_SHEET_ID:
        errors.append("  ❌ GOOGLE_SHEET_ID — bo'sh! (Google Sheets URL dan oling)")

    # MUHIM: Faylni emas, Railway'dagi matnni tekshiramiz!
    if not config.GOOGLE_CREDENTIALS:
        errors.append(
            "  ❌ GOOGLE_CREDENTIALS — topilmadi! "
            "(Railway Variables ga JSON matnini kiriting)"
        )

    if errors:
        logger.error("=" * 55)
        logger.error("BOT ISHGA TUSHMADI — sozlamalar xato!")
        logger.error("=" * 55)
        for err in errors:
            logger.error(err)
        logger.error("=" * 55)
        sys.exit(1)


# ─── Bot va Dispatcher ─────────────────────────────────────────────────────────
def _build_bot_and_dp() -> tuple[Bot, Dispatcher]:
    bot = Bot(
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(start_router)         
    dp.include_router(registration_router)  
    dp.include_router(contact_router)  
    dp.include_router(admin_router)     

    return bot, dp


# ─── Startup ───────────────────────────────────────────────────────────────────
async def on_startup(bot: Bot) -> None:
    me = await bot.get_me()
    logger.info("=" * 55)
    logger.info("Bot ishga tushdi!")
    logger.info("  Nomi    : %s", me.full_name)
    logger.info("  Username: @%s", me.username)
    logger.info("  ID      : %d", me.id)
    logger.info("=" * 55)

    logger.info("Google Sheets ulanish tekshirilmoqda...")
    sheets_ok = await check_sheets_connection()

    if not sheets_ok:
        logger.error("=" * 55)
        logger.error("KRITIK XATO: Google Sheets ga ulanib bo'lmadi!")
        logger.error("Quyidagilarni tekshiring:")
        logger.error("  1. GOOGLE_CREDENTIALS Railway'ga to'g'ri kiritilganmi?")
        logger.error("  2. Service account emaili Sheets ga qo'shilganmi? (Editor)")
        logger.error("  3. GOOGLE_SHEET_ID to'g'rimi?")
        logger.error("=" * 55)
        raise RuntimeError("Google Sheets ga ulanib bo'lmadi.")

    logger.info("Barcha tekshiruvlar o'tdi ✓")
    logger.info("Bot buyurtmalarni qabul qilishga tayyor! 🍓")
    logger.info("=" * 55)


# ─── Shutdown ──────────────────────────────────────────────────────────────────
async def on_shutdown(bot: Bot) -> None:
    logger.info("Bot to'xtatilmoqda...")
    await bot.session.close()
    logger.info("Bot to'xtatildi.")


# ─── Asosiy funksiya ───────────────────────────────────────────────────────────
async def main() -> None:
    _check_env()
    bot, dp = _build_bot_and_dp()

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    logger.info("Polling boshlandi…")
    await dp.start_polling(
        bot,
        allowed_updates=dp.resolve_used_update_types(),
    )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except RuntimeError as e:
        logger.critical("Bot ishga tushirilmadi: %s", e)
        sys.exit(1)
    except KeyboardInterrupt:
        logger.info("Foydalanuvchi tomonidan to'xtatildi (Ctrl+C).")