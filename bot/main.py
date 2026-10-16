import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from .config import BOT_TOKEN
from .handlers import main_router

# Log tizimini sozlash
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


async def main():
    if not BOT_TOKEN or BOT_TOKEN == "your_telegram_bot_token_here":
        logger.error(
            "XATOLIK: BOT_TOKEN aniqlanmadi! "
            "Iltimos, .env faylini oching va unga Telegram bot tokeningizni kiriting."
        )
        print("\n" + "=" * 60)
        print("XATOLIK: .env faylida BOT_TOKEN mavjud emas!")
        print("1. .env faylini yarating yoki .env.example dan nusxa oling.")
        print("2. @BotFather dan olingan bot tokeningizni kiriting.")
        print("=" * 60 + "\n")
        return

    logger.info("Bot ishga tushirilmoqda...")

    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()

    # Routerlarni ulash
    dp.include_router(main_router)

    # Eski kutilayotgan yangilanishlarni (updates) o'chirib tashlash
    await bot.delete_webhook(drop_pending_updates=True)

    logger.info("Bot muvaffaqiyatli ishga tushdi va xabarlarni kutmoqda!")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot to'xtatildi.")
