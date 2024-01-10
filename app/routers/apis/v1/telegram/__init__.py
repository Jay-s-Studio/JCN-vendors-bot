"""
Top level router for telegram API
"""
from fastapi import APIRouter

from .messages import router as message_router

router = APIRouter()
router.include_router(message_router, prefix="/messages", tags=["Telegram Messages"])
