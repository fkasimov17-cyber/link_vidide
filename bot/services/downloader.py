import asyncio
import logging
import os
import uuid
from pathlib import Path
from typing import Dict, Any, Optional
import yt_dlp

from ..config import DOWNLOAD_DIR, MAX_FILE_SIZE_BYTES
from ..utils.helpers import identify_platform, format_duration

logger = logging.getLogger(__name__)


class VideoDownloader:
    """
    Turli platformalardan (YouTube, Instagram, TikTok, Pinterest, Facebook, X)
    videolarni yuklab oluvchi servis sinfi.
    """

    @staticmethod
    def _extract_info_sync(url: str) -> Dict[str, Any]:
        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "skip_download": True,
            "nocheckcertificate": True,
            "socket_timeout": 15,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            return ydl.extract_info(url, download=False)

    @classmethod
    async def get_metadata(cls, url: str) -> Optional[Dict[str, Any]]:
        """
        Video haqidagi dastlabki ma'lumotlarni asinxron tarzda oladi.
        """
        try:
            info = await asyncio.to_thread(cls._extract_info_sync, url)
            if not info:
                return None

            title = info.get("title") or "Noma'lum sarlavha"
            duration = info.get("duration")
            platform = identify_platform(url)

            return {
                "title": title,
                "duration_formatted": format_duration(duration),
                "duration_raw": duration,
                "platform": platform,
                "thumbnail": info.get("thumbnail"),
                "uploader": info.get("uploader") or info.get("channel"),
            }
        except Exception as e:
            logger.error(f"Metama'lumot olishda xatolik: {e}")
            return None

    @staticmethod
    def _download_sync(url: str, output_path: str) -> Dict[str, Any]:
        ydl_opts = {
            "outtmpl": output_path,
            # Telegram limiti (50MB) doirasidagi eng yaxshi sifatni tanlash
            "format": (
                "b[filesize<=48M]/"
                "best[ext=mp4][filesize<=48M]/"
                "bestvideo[filesize<=40M]+bestaudio/"
                "best[ext=mp4]/"
                "best"
            ),
            "quiet": True,
            "no_warnings": True,
            "nocheckcertificate": True,
            "merge_output_format": "mp4",
            "socket_timeout": 30,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            # Haqiqiy saqlangan fayl yo'lini aniqlash
            filename = ydl.prepare_filename(info)
            # Agar format o'zgargan bo'lsa (masalan mp4 ga merge qilingan bo'lsa)
            base_without_ext = os.path.splitext(filename)[0]
            if os.path.exists(f"{base_without_ext}.mp4"):
                actual_file = f"{base_without_ext}.mp4"
            elif os.path.exists(filename):
                actual_file = filename
            else:
                # Papkadagi mos faylni qidirish
                matched = list(Path(output_path).parent.glob(f"{Path(output_path).stem}.*"))
                actual_file = str(matched[0]) if matched else filename

            return {
                "file_path": actual_file,
                "title": info.get("title") or "Video",
                "duration": info.get("duration"),
            }

    @classmethod
    async def download(cls, url: str) -> Optional[Dict[str, Any]]:
        """
        Videoni asinxron yuklab oladi va fayl ma'lumotlarini qaytaradi.
        """
        unique_id = uuid.uuid4().hex[:10]
        output_template = str(DOWNLOAD_DIR / f"vid_{unique_id}.%(ext)s")

        try:
            result = await asyncio.to_thread(cls._download_sync, url, output_template)
            file_path = result.get("file_path")

            if file_path and os.path.exists(file_path):
                file_size = os.path.getsize(file_path)
                result["file_size"] = file_size

                # Telegram 50MB limitini tekshirish
                if file_size > MAX_FILE_SIZE_BYTES:
                    cls.delete_file(file_path)
                    return {
                        "error": "too_large",
                        "size": file_size,
                    }

                return result
            return None
        except Exception as e:
            logger.error(f"Videoni yuklab olishda xatolik: {e}")
            return None

    @staticmethod
    def delete_file(file_path: Optional[str]) -> None:
        """
        Yuborilganidan so'ng vaqtinchalik video faylni xavfsiz o'chiradi.
        """
        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as e:
                logger.warning(f"Faylni o'chirishda xatolik: {e}")
