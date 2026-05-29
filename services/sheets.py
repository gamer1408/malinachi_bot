"""
Google Sheets integratsiyasi — 4-bosqich (Railway uchun to'liq tozalangan).

Kutubxonalar:
    gspread==6.0.0
    google-auth==2.28.0
"""
import json
import logging
from datetime import datetime, timezone, timedelta

import gspread
from google.oauth2.service_account import Credentials

import config

logger = logging.getLogger(__name__)

# ─── OAuth2 scope'lari ─────────────────────────────────────────────────────────
_SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

# ─── O'zbekiston vaqt zonasi UTC+5 ────────────────────────────────────────────
_UZ_TZ = timezone(timedelta(hours=5))

# ─── Worksheet nomi ───────────────────────────────────────────────────────────
_WORKSHEET_NAME = "Buyurtmalar"


def _get_client() -> gspread.client.Client:
    """
    Railway'dagi GOOGLE_CREDENTIALS muhit o'zgaruvchisidan JSON ni o'qib,
    gspread mijozini (client) qaytaradi.
    """
    if not config.GOOGLE_CREDENTIALS:
        raise ValueError("GOOGLE_CREDENTIALS muhit o'zgaruvchisi topilmadi yoki bo'sh!")
    
    try:
        creds_dict = json.loads(config.GOOGLE_CREDENTIALS)
    except json.JSONDecodeError as e:
        raise ValueError(f"GOOGLE_CREDENTIALS ichidagi JSON formati noto'g'ri: {e}")

    creds = Credentials.from_service_account_info(creds_dict, scopes=_SCOPES)
    return gspread.authorize(creds)


def _get_worksheet() -> gspread.Worksheet:
    """
    Google Sheets ga ulanib, ishchi sahifani qaytaradi.
    Sahifa mavjud bo'lmasa yangi yaratadi.
    """
    client = _get_client()
    spreadsheet = client.open_by_key(config.GOOGLE_SHEET_ID)

    try:
        worksheet = spreadsheet.worksheet(_WORKSHEET_NAME)
    except gspread.WorksheetNotFound:
        worksheet = spreadsheet.add_worksheet(
            title=_WORKSHEET_NAME,
            rows=1000,
            cols=len(config.SHEET_COLUMNS),
        )
        logger.info("Yangi worksheet yaratildi: '%s'", _WORKSHEET_NAME)

    return worksheet


def _ensure_header(worksheet: gspread.Worksheet) -> None:
    """
    Birinchi qator header ekanligini tekshiradi.
    Bo'sh yoki noto'g'ri bo'lsa — to'g'ri header yozadi.
    """
    try:
        first_row = worksheet.row_values(1)
    except Exception:
        first_row = []

    if first_row != config.SHEET_COLUMNS:
        worksheet.update(
            range_name="A1",
            values=[config.SHEET_COLUMNS],
        )
        try:
            worksheet.format(
                f"A1:{chr(64 + len(config.SHEET_COLUMNS))}1",
                {
                    "textFormat": {"bold": True},
                    "backgroundColor": {"red": 0.85, "green": 0.93, "blue": 0.83},
                },
            )
        except Exception as fmt_err:
            logger.warning("Header formatlanmadi: %s", fmt_err)

        logger.info("Header qator yozildi: %s", config.SHEET_COLUMNS)


def _next_row_number(worksheet: gspread.Worksheet) -> int:
    """
    Joriy buyurtmalar sonini hisoblab, keyingi tartib raqamni qaytaradi.
    (Header — 1-qator, data 2-qatordan boshlanadi)
    """
    all_values = worksheet.get_all_values()
    data_rows = len(all_values) - 1 if len(all_values) > 0 else 0
    return max(data_rows + 1, 1)


async def save_to_sheets(user_data: dict) -> bool:
    """
    Buyurtma ma'lumotlarini Google Sheets ga saqlaydi.
    """
    try:
        now_uz = datetime.now(tz=_UZ_TZ)
        sana = now_uz.strftime("%d.%m.%Y %H:%M")

        worksheet = _get_worksheet()
        _ensure_header(worksheet)

        order_number = _next_row_number(worksheet)

        row = [
            order_number,
            sana,
            user_data.get("user_id", ""),
            user_data.get("username", "—"),
            user_data.get("name", ""),
            user_data.get("region", ""),
            user_data.get("quantity", ""),
            user_data.get("phone", ""),
            config.OrderStatus.NEW,
        ]

        worksheet.append_row(
            row,
            value_input_option="USER_ENTERED",
        )

        logger.info(
            "Google Sheets ga saqlandi: №%d | %s | %s | %s",
            order_number,
            user_data.get("name"),
            user_data.get("region"),
            user_data.get("phone"),
        )
        return True

    except ValueError as ve:
        logger.error("JSON sozlamalari xatosi: %s", ve)
        return False
    except gspread.exceptions.APIError as api_err:
        logger.error("Google Sheets API xatosi: %s", api_err)
        return False
    except gspread.exceptions.SpreadsheetNotFound:
        logger.error(
            "Google Sheets topilmadi! GOOGLE_SHEET_ID: %s",
            config.GOOGLE_SHEET_ID,
        )
        return False
    except Exception as exc:
        logger.error("save_to_sheets kutilmagan xato: %s", exc, exc_info=True)
        return False


async def check_sheets_connection() -> bool:
    """
    on_startup da Google Sheets ulanishni tekshirish uchun.
    Fayldan emas, Railway'dagi muhit o'zgaruvchisidan o'qiydi.
    """
    try:
        client = _get_client()
        spreadsheet = client.open_by_key(config.GOOGLE_SHEET_ID)
        _ = spreadsheet.title
        logger.info("Google Sheets ulanish tekshirildi: OK ✓ ('%s')", spreadsheet.title)
        return True
        
    except ValueError as ve:
        logger.error("STARTUP XATO (JSON): %s", ve)
        return False
    except gspread.exceptions.SpreadsheetNotFound:
        logger.error(
            "STARTUP XATO: Google Sheet topilmadi. GOOGLE_SHEET_ID=%s",
            config.GOOGLE_SHEET_ID,
        )
        return False
    except gspread.exceptions.APIError as e:
        logger.error("STARTUP XATO: Google Sheets API xatosi: %s", e)
        return False
    except Exception as e:
        logger.error("STARTUP XATO: Google Sheets ulanish kutilmagan xatosi: %s", e, exc_info=True)
        return False