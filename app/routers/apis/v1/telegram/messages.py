"""
Telegram Router
"""
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from starlette import status

from app.containers import Container
from app.handlers.telegram import TelegramMessagesHandler
from app.serializers.v1.telegram import PaymentAccount

router = APIRouter()


@router.post(
    path="/exchange_rate_msg",
    status_code=status.HTTP_200_OK
)
@inject
async def exchange_rate_msg(
    telegram_messages_handler: TelegramMessagesHandler = Depends(Provide[Container.telegram_messages_handler])
):
    """

    :param telegram_messages_handler:
    :return:
    """
    await telegram_messages_handler.exchange_rate_msg()
    return {"message": "success"}


@router.post(
    path="/payment_account",
)
@inject
async def payment_account(
    model: PaymentAccount,
    telegram_messages_handler: TelegramMessagesHandler = Depends(Provide[Container.telegram_messages_handler])
):
    """

    :param model:
    :param telegram_messages_handler:
    :return:
    """
    return await telegram_messages_handler.payment_account(model)
