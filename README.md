# 🎬 Universal Video Downloader Telegram Bot

Ushbu bot barcha ommabop ijtimoiy tarmoqlar va video platformalardan videolarni metama'lumotlari bilan birga avtomatik tarzda tahlil qilib, eng yuqori sifatda yuklab beradi.

---

## 🌟 Qo'llab-quvvatlanadigan Platformalar

- 🔴 **YouTube** (Shorts va to'liq videolar)
- 📸 **Instagram** (Reels, postlar va IGTV)
- 🎵 **TikTok** (Suv belgisisiz / No watermark)
- 📌 **Pinterest** (Video pinlar)
- 🔵 **Facebook** (Watch va Reels)
- 🐦 **X (Twitter)** (Barcha video postlar)

---

## 📁 Loyiha Strukturasi

```text
├── bot/
│   ├── handlers/
│   │   ├── __init__.py
│   │   ├── start.py        # /start va /help buyruqlari
│   │   └── video.py        # Havolalarni qabul qilish va video yuborish
│   ├── services/
│   │   ├── __init__.py
│   │   └── downloader.py   # yt-dlp asosidagi universal yuklovchi
│   ├── utils/
│   │   ├── __init__.py
│   │   └── helpers.py      # Platforma va vaqtni formatlash
│   ├── __init__.py
│   ├── config.py           # Sozlamalar va .env integratsiyasi
│   └── main.py             # Botning asosiy ishga tushirish qismi
├── .github/
│   └── workflows/
│       └── deploy.yml      # CI/CD avtomatik deploy
├── .env.example            # Token va sozlamalar shabloni
├── .gitignore              # Maxfiy fayllar va .env ni himoyalash
├── bot.service             # Linux systemd (24/7) servisi
├── Dockerfile              # Docker konteyner fayli
├── docker-compose.yml      # Docker compose konfiguratsiyasi
├── requirements.txt        # Kerakli Python kutubxonalari
├── run.py                  # Tezkor ishga tushirish fayli
└── README.md               # To'liq qo'llanma
```

---

## 🚀 1. Lokal Muhitda Ishga Tushirish

### 1-qadam: Virtual muhit (venv) yaratish va faollashtirish
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 2-qadam: Kutubxonalarni o'rnatish
```bash
pip install -r requirements.txt
```

### 3-qadam: .env faylini yaratish
`.env.example` faylidan nusxa olib `.env` nomli fayl yarating:
```env
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
MAX_FILE_SIZE_MB=50
```

### 4-qadam: Botni ishga tushirish
```bash
python run.py
```

---

## 🐙 2. GitHub Repozitoriyasiga Joylash (Push)

> ⚠️ **MUHIM XAVFSIZLIK QOIDASI:**
> `.env` fayli va bot tokeningizni hech qachon GitHub'ga ommaviy joylamang. Loyihadagi `.gitignore` fayli buni avtomatik tarzda himoyalaydi.

```bash
# 1. Git repozitoriyasini boshlash
git init

# 2. Asosiy tarmoqni main ga o'zgartirish
git branch -M main

# 3. Fayllarni indeksga qo'shish
git add .

# 4. Ilk commit yaratish
git commit -m "feat: initial commit for universal video downloader bot"

# 5. O'zingizning GitHub repozitoriyangizni ulash
git remote add origin https://github.com/USERNAME/REPO_NAME.git

# 6. Kodni GitHub'ga yuklash
git push -u origin main
```

---

## 🖥 3. Serverga (VPS / Ubuntu) O'rnatish (24/7 Ishlatish)

### A) Serverni tayyorlash
```bash
# Paketlarni yangilash va ffmpeg o'rnatish (juda muhim)
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip python3-venv git ffmpeg -y

# Papka yaratish va kodni klonlash
sudo mkdir -p /var/www/bot
sudo chown -R $USER:$USER /var/www/bot
git clone https://github.com/USERNAME/REPO_NAME.git /var/www/bot
cd /var/www/bot

# Virtual muhit va kutubxonalar
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# .env faylini yaratish
nano .env
# BOT_TOKEN ni yozib, CTRL+O va CTRL+X bosing
```

### B) Systemd orqali 24/7 rejimida yoqish
```bash
# Servis faylini tizimga ko'chirish
sudo cp bot.service /etc/systemd/system/bot.service

# Servislarni yangilash va ishga tushirish
sudo systemctl daemon-reload
sudo systemctl enable bot.service
sudo systemctl start bot.service

# Bot holatini ko'rish
sudo systemctl status bot.service
```

---

## 🐳 4. Docker Orqali Ishga Tushirish (1-Buyruq Bilan)

Agar serveringizda Docker o'rnatilgan bo'lsa:
```bash
# .env faylini yarating va tokenni kiriting
cp .env.example .env
nano .env

# Konteynerni orqa fonda ishga tushirish
docker compose up -d --build

# Loglarni jonli kuzatish
docker compose logs -f
```

---

## 🔄 5. CI/CD (GitHub Actions)

Loyiha `.github/workflows/deploy.yml` fayli bilan ta'minlangan.
GitHub omboringizning **Settings -> Secrets and variables -> Actions** bo'limida quyidagi maxfiy kalitlarni kiriting:
- `VPS_HOST` - Serveringiz IP manzili
- `VPS_USER` - Server foydalanuvchisi (masalan `root` yoki `ubuntu`)
- `VPS_SSH_KEY` - Serveringiz SSH maxfiy kaliti
- `VPS_PORT` - SSH porti (standart `22`)

Har safar `main` tarmog'iga o'zgarish yuklanganda, bot avtomatik tarzda serverda yangilanadi va qayta ishga tushadi.
