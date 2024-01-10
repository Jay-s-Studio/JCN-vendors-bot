"""
Top level router for v1 API
"""
from fastapi import APIRouter

from .telegram import router as telegram_router

router = APIRouter()
router.include_router(telegram_router)
