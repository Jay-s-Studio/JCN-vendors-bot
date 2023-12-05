"""
Telegram Router
"""
import telegram
from fastapi import APIRouter, HTTPException

from app.bot import bot
from app.serializers.v1.telegram import TelegramBroadcast

router = APIRouter()


@router.post(
    path="/broadcast"
)
async def broadcast(
    model: TelegramBroadcast,
):
    """

    :param model:
    :return:
    """
    try:
        message = await bot.send_message(chat_id=model.chat_id, text=model.message)
    except telegram.error.BadRequest as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return message.to_dict()
