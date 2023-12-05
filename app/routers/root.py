"""
Root router.
"""
from fastapi import APIRouter
from .v1 import router as v1_router

router = APIRouter(prefix="/api")
router.include_router(v1_router, prefix="/v1", tags=["v1"])


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
