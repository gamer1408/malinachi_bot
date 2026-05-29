# Malinachi.uz Bot — Ishga tushirish yo'riqnomasi

## Fayl tuzilmasi

```
malinachi_bot_stage4/
├── main.py                  ← Asosiy fayl (shu yerdan boshlanadi)
├── config.py                ← Barcha sozlamalar
├── states.py                ← FSM holatlari
├── keyboards.py             ← Tugmalar
├── requirements.txt         ← Python kutubxonalar
├── Dockerfile               ← Docker image
├── docker-compose.yml       ← Docker Compose
├── .env.example             ← .env namunasi (buni nusxalab .env yarating)
├── .gitignore
├── handlers/
│   ├── start.py             ← /start komandasi
│   ├── registration.py      ← Ism → Viloyat → Miqdor
│   └── contact.py          ← Telefon → Yakunlash
└── services/
    ├── sheets.py            ← Google Sheets saqlash + tekshirish
    └── notifier.py         ← Admin kanal xabari
```

---

## 1-QADAM: Bot token olish

1. Telegramda **@BotFather** ga yozing
2. `/newbot` yuboring
3. Bot nomi va username kiriting
4. Olingan tokenni saqlang: `1234567890:AAxxx...`

---

## 2-QADAM: credentials.json olish (Google Service Account)

1. **Google Cloud Console** ga kiring: https://console.cloud.google.com
2. Yangi loyiha yarating (yoki mavjudini tanlang)
3. **API va Xizmatlar** → **API kutubxonasi**:
   - `Google Sheets API` — yoqing ✓
   - `Google Drive API` — yoqing ✓
4. **API va Xizmatlar** → **Ma'lumotlar** → **Ma'lumot yaratish** → **Xizmat hisob qaydnomasi**
5. Nom kiriting, `Yaratish` bosing
6. **Kalitlar** yorlig'i → **Kalit qo'shish** → **Yangi kalit yaratish** → **JSON**
7. Yuklab olingan faylni `credentials.json` deb loyiha papkasiga saqlang

---

## 3-QADAM: Google Sheet tayyorlash

1. **Google Sheets** oching: https://sheets.google.com
2. Yangi jadval yarating
3. URL dan ID ni nusxalang:
   ```
   https://docs.google.com/spreadsheets/d/  →→  1BxiMVs0XRA5nFMd...  ←←  /edit
   ```
4. **Ulashish** tugmasini bosing → credentials.json dagi `client_email` manzilini qo'shing
   - `client_email` ni `credentials.json` dan topishingiz mumkin
   - **Editor** huquqini bering
5. Bot birinchi buyurtmada avtomatik ravishda "Buyurtmalar" nomli sahifa va header yaratadi

---

## 4-QADAM: Admin kanal ID topish

### Usul 1 — @userinfobot orqali
1. Kanalingizdan istalgan xabarni **@userinfobot** ga forward qiling
2. Bot kanal ID ni ko'rsatadi (masalan: `-1001234567890`)

### Usul 2 — Vaqtinchalik bot orqali
1. Botingizni kanalga **Admin** qiling (xabar yuborish huquqi bilan)
2. Kanalga `/start` yuboring
3. `https://api.telegram.org/bot<TOKEN>/getUpdates` ni brauzerda oching
4. `chat.id` qiymatini oling

### Usul 3 — @username_to_id_bot
- Kanaldan xabar forward qiling, bot ID ni beradi

---

## 5-QADAM: .env faylini to'ldirish

```bash
cp .env.example .env
```

`.env` faylini tahrirlang:
```env
BOT_TOKEN=1234567890:AAxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
ADMIN_CHANNEL_ID=-1001234567890
GOOGLE_SHEET_ID=1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgVE2upms
```

---

## 6-QADAM: Botni ishga tushirish

### Variant A — Python bilan (lokal)

```bash
# Virtual muhit yarating
python -m venv .venv
source .venv/bin/activate        # Linux/Mac
# yoki
.venv\Scripts\activate           # Windows

# Kutubxonalarni o'rnating
pip install -r requirements.txt

# Ishga tushiring
python main.py
```

Muvaffaqiyatli ishga tushsa log:
```
Bot ishga tushdi!
  Nomi    : Malinachi Bot
  Username: @malinachi_uz_bot
  ID      : 1234567890
Google Sheets ulanish tekshirildi: OK ✓
Bot buyurtmalarni qabul qilishga tayyor! 🍓
```

### Variant B — Docker Compose bilan (server)

```bash
# Fayllar joylashuvi (server papkasida):
# .env
# credentials.json
# docker-compose.yml
# Dockerfile
# ... (barcha kod fayllar)

# Ishga tushirish
docker-compose up -d

# Loglarni ko'rish
docker-compose logs -f

# To'xtatish
docker-compose down
```

---

## Xato xabarlari va yechimlari

| Xato | Sabab | Yechim |
|------|-------|--------|
| `BOT_TOKEN — bo'sh` | .env to'ldirilmagan | .env ga token kiriting |
| `credentials.json topilmadi` | Fayl yo'q | Google Cloud dan yuklab oling |
| `Google Sheets topilmadi` | Noto'g'ri ID yoki ruxsat | Sheet ID va email ulashishni tekshiring |
| `Telegram API xatosi (admin kanal)` | Bot kanal admin emas | Botni kanalga admin qiling |
| `GOOGLE_SHEET_ID — bo'sh` | .env to'ldirilmagan | Sheets URL dan ID nusxalang |

---

## Tekshirish ro'yxati (ishga tushirishdan oldin)

- [ ] `.env` fayli yaratilgan va to'ldirilgan
- [ ] `credentials.json` loyiha papkasida bor
- [ ] Google Sheets API va Drive API yoqilgan
- [ ] Service account email Sheets ga qo'shilgan (Editor)
- [ ] Bot kanalga Admin qilingan (xabar yuborish huquqi bilan)
- [ ] `ADMIN_CHANNEL_ID` to'g'ri (manfiy son)

---

## Foydalanish

Bot ishga tushgach foydalanuvchi:
1. `/start` → Xush kelibsiz xabari
2. Ism kiriting
3. Viloyatni tanlang (tugmalardan)
4. Ko'chat miqdorini tanlang (tugmalardan)
5. Telefon raqam yuboring (tugma yoki qo'lda)
6. ✅ Buyurtma qabul qilindi

Natija:
- Google Sheets → "Buyurtmalar" sahifasiga yangi qator qo'shiladi
- Admin kanal → HTML formatdagi xabar keladi
