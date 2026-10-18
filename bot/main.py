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

    import os
    from aiogram.client.session.aiohttp import AiohttpSession
    from aiohttp import ClientSession, TCPConnector

    class ResilientSession(AiohttpSession):
        async def create_session(self) -> ClientSession:
            if self._session is None or self._session.closed:
                # Windows yoki maxsus korporativ tarmoqlarda SSL muammosini oldini olish
                if os.name == "nt":
                    connector = TCPConnector(ssl=False)
                else:
                    connector = TCPConnector()
                self._session = ClientSession(connector=connector)
            return self._session

    bot = Bot(
        token=BOT_TOKEN,
        session=ResilientSession(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()

    # Routerlarni ulash
    dp.include_router(main_router)

    # Render.com yoki boshqa bulutli xizmatlarning bepul Web Service rejimi uchun (health check)
    port = os.getenv("PORT")
    if port:
        from aiohttp import web
        app = web.Application()
        async def handle_ping(request):
            return web.Response(text="Link Vidide Bot is running!")
        app.router.add_get("/", handle_ping)
        app.router.add_get("/health", handle_ping)
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, "0.0.0.0", int(port))
        await site.start()
        logger.info(f"Health-check veb-server {port}-portda ishga tushdi.")

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
