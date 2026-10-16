import re
from urllib.parse import urlparse


def identify_platform(url: str) -> str:
    """
    Havola domeniga qarab video platformasini aniqlaydi.
    """
    try:
        domain = urlparse(url).netloc.lower()
    except Exception:
        domain = ""

    if any(d in domain for d in ["youtube.com", "youtu.be"]):
        if "/shorts/" in url:
            return "YouTube Shorts"
        return "YouTube"
    elif "instagram.com" in domain:
        if "/reel/" in url or "/reels/" in url:
            return "Instagram Reels"
        return "Instagram"
    elif any(d in domain for d in ["tiktok.com", "vt.tiktok.com"]):
        return "TikTok"
    elif any(d in domain for d in ["pinterest.com", "pin.it"]):
        return "Pinterest"
    elif any(d in domain for d in ["facebook.com", "fb.watch", "fb.com"]):
        return "Facebook"
    elif any(d in domain for d in ["twitter.com", "x.com"]):
        return "X (Twitter)"

    return "Boshqa Platforma"


def format_duration(seconds: int | float | None) -> str:
    """
    Sekundlarni MM:SS yoki HH:MM:SS formatiga o'tkazadi.
    """
    if not seconds or seconds < 0:
        return "Noma'lum"

    seconds = int(seconds)
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60

    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


def format_size(size_bytes: int | float | None) -> str:
    """
    Baytlarni o'qilishi oson formatga (MB/KB) o'tkazadi.
    """
    if not size_bytes:
        return "Noma'lum"

    mb = size_bytes / (1024 * 1024)
    if mb >= 1.0:
        return f"{mb:.2f} MB"
    kb = size_bytes / 1024
    return f"{kb:.1f} KB"
