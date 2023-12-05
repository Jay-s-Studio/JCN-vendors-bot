"""Demo Router"""
from fastapi import APIRouter
from starlette.requests import Request

router = APIRouter()


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
