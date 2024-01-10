"""Demo Router"""
from fastapi import APIRouter
from starlette.requests import Request

from app.routing import LogRouting

router = APIRouter(route_class=LogRouting)


@router.get(
    path=""
)
async def get_demo(
    request: Request,
):
    """

    :param request:
    :return:
    """
    return {
        "message": "Hello World!"
    }
