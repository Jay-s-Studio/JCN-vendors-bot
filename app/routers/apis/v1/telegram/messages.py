"""
Telegram Router
"""
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from starlette import status

from app.containers import Container
from app.handlers.telegram import TelegramHandler
from app.serializers.v1.telegram import TelegramBroadcast

router = APIRouter()


@router.post(
    path="/broadcast"
)
@inject
async def broadcast(
    model: TelegramBroadcast,
    telegram_handler: TelegramHandler = Depends(Provide[Container.telegram_handler])
):
    """

    :param model:
    :param telegram_handler:
    :return:
    """
    return await telegram_handler.broadcast_message(model)


@router.post(
    path="/exchange_rate_msg",
    status_code=status.HTTP_200_OK
)
@inject
async def exchange_rate_msg(
    telegram_handler: TelegramHandler = Depends(Provide[Container.telegram_handler])
):
    """

    :param telegram_handler:
    :return:
    """
    await telegram_handler.exchange_rate_msg()
    return {"message": "success"}
