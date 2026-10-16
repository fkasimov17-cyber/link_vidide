import re
import logging
from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.enums import ChatAction

from ..services.downloader import VideoDownloader
from ..utils.helpers import identify_platform, format_size

logger = logging.getLogger(__name__)
router = Router()

# URL qidirish uchun regex
URL_REGEX = re.compile(
    r"(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|"
    r"https?:\/\/[a-zA-Z0-9]+\.[^\s]{2,})"
)


@router.message(F.text)
async def handle_text_message(message: Message):
    text = message.text.strip()

    # Matn ichidan URL ni qidirish
    url_match = URL_REGEX.search(text)

    if not url_match:
        # Agar havola bo'lmasa, talab qilingan ogohlantirishni chiqaramiz
        await message.reply(
            "Iltimos, video havolasini (link) yuboring yoki GitHub/Server so'rovini kiriting."
        )
        return

    url = url_match.group(0)
    platform = identify_platform(url)

    # 1. Havolani qabul qilinganligi haqida bildirish
    status_msg = await message.reply("🔍 *Video ma'lumotlari tahlil qilinmoqda...*", parse_mode="Markdown")

    try:
        # Chat action (typing/uploading video)
        await message.bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.RECORD_VIDEO)

        # 2. Metama'lumotlarni olish
        metadata = await VideoDownloader.get_metadata(url)
        title = metadata.get("title", "Noma'lum sarlavha") if metadata else "Video"
        duration = metadata.get("duration_formatted", "Noma'lum") if metadata else "Noma'lum"

        # Belgilangan aniq format bo'yicha xabarni tahrirlash
        info_text = (
            f"🎬 **Video muvaffaqiyatli topildi!**\n"
            f"📌 **Manba:** {platform}\n"
            f"📝 **Sarlavha:** {title}\n"
            f"⏱ **Davomiyligi:** {duration}\n\n"
            f"⬇️ *Sizning videongiz yuklanmoqda...*"
        )
        await status_msg.edit_text(info_text, parse_mode="Markdown")

        # 3. Videoni serverga yuklab olish
        await message.bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.UPLOAD_VIDEO)
        download_result = await VideoDownloader.download(url)

        if not download_result:
            await status_msg.edit_text(
                "❌ **Kechirasiz, videoni yuklab olishning imkoni bo'lmadi.**\n"
                "Havola yopiq (private) bo'lishi yoki platforma cheklovi o'rnatilgan bo'lishi mumkin.",
                parse_mode="Markdown"
            )
            return

        if download_result.get("error") == "too_large":
            size_str = format_size(download_result.get("size"))
            await status_msg.edit_text(
                f"⚠️ **Video hajmi juda katta!** ({size_str})\n"
                f"Telegram Bot API limiti 50 MB gacha bo'lgan videolarni yuborishga ruxsat beradi.",
                parse_mode="Markdown"
            )
            return

        file_path = download_result.get("file_path")
        video_file = FSInputFile(file_path)

        # 4. Foydalanuvchiga videoni yuborish
        caption = f"🎬 **{title}**\n\n📌 *Manba:* {platform}"
        # Telegram sarlavha uzunligi 1024 belgi
        if len(caption) > 1000:
            caption = caption[:997] + "..."

        await message.answer_video(
            video=video_file,
            caption=caption,
            parse_mode="Markdown",
            supports_streaming=True
        )

        # Holat xabarini tozalash (yoki o'chirish)
        try:
            await status_msg.delete()
        except Exception:
            pass

        # 5. Vaqtinchalik faylni xavfsiz o'chirish
        VideoDownloader.delete_file(file_path)

    except Exception as e:
        logger.error(f"Xatolik yuz berdi: {e}", exc_info=True)
        try:
            await status_msg.edit_text(
                "❌ **Videoni yuklab yuborishda kutilmagan xatolik yuz berdi.**\n"
                "Iltimos, boshqa havola orqali qayta urinib ko'ring.",
                parse_mode="Markdown"
            )
        except Exception:
            pass
