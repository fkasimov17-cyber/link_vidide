from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    text = (
        "👋 **Assalomu alaykum!**\n\n"
        "Men ijtimoiy tarmoqlardan videolarni qulay va tez yuklab beruvchi universal botman.\n\n"
        "⚡ **Qo'llab-quvvatlanadigan platformalar:**\n"
        "• 🔴 **YouTube** (Shorts va videolar)\n"
        "• 📸 **Instagram** (Reels va postlar)\n"
        "• 🎵 **TikTok** (Suv belgisisiz)\n"
        "• 📌 **Pinterest**\n"
        "• 🔵 **Facebook**\n"
        "• 🐦 **X (Twitter)**\n\n"
        "🔗 *Menga shunchaki video havolasini (link) yuboring!*"
    )
    await message.answer(text, parse_mode="Markdown")


@router.message(Command("help"))
async def cmd_help(message: Message):
    text = (
        "ℹ️ **Qo'llanma:**\n\n"
        "1. Istalgan ijtimoiy tarmoqdan video havolasini nusxalang.\n"
        "2. Havolani ushbu botga xabar sifatida yuboring.\n"
        "3. Bot videoni tahlil qilib, sizga to'g'ridan-to'g'ri yuboradi.\n\n"
        "⚠️ *Telegram Bot API limiti: 50 MB gacha bo'lgan videolarni yuklaydi.*"
    )
    await message.answer(text, parse_mode="Markdown")
