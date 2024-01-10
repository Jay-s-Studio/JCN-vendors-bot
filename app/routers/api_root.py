"""
Root router.
"""
from fastapi import APIRouter
from .apis.v1 import router as api_v1_router

router = APIRouter()
router.include_router(api_v1_router, prefix="/v1", tags=["API v1"])


@router.get(
    path="/healthcheck"
)
async def healthcheck():
    """
    Healthcheck endpoint
    :return:
    """
    return {
        "message": "ok"
    }
