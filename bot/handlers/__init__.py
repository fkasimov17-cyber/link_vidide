from aiogram import Router
from .start import router as start_router
from .video import router as video_router

main_router = Router()
main_router.include_router(start_router)
main_router.include_router(video_router)

__all__ = ["main_router"]
