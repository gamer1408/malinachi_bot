FROM python:3.11-slim

# Vaqt zonasini o'rnatish (o'zingiz uchun loglarda qulay)
ENV TZ=Asia/Tashkent

WORKDIR /app

# Avval faqat requirements — Docker cache dan foydalanish uchun
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Qolgan barcha fayllarni ko'chirish
COPY . .

# credentials.json va .env — volume yoki env_file orqali beriladi
# (bu yerda COPY qilinmaydi — xavfsizlik uchun)

CMD ["python", "main.py"]
