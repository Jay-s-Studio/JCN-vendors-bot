"""
Webhook root router.
"""
from fastapi import APIRouter
from .webhooks.v1 import router as webhook_v1_router

router = APIRouter()
router.include_router(webhook_v1_router, prefix="/v1", tags=["Webhook v1"])
