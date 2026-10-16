FROM python:3.11-slim

# Tizim paketlarini yangilash va ffmpeg o'rnatish
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Bog'liqliklarni o'rnatish
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Loyiha fayllarini ko'chirish
COPY . .

# Yuklab olishlar uchun papkani yaratish
RUN mkdir -p downloads

# Botni ishga tushirish
CMD ["python", "run.py"]
