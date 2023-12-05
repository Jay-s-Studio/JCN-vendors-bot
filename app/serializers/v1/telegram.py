"""
Serializers for Telegram API
"""
from pydantic import BaseModel


class TelegramBroadcast(BaseModel):
    """
    Telegram Broadcast
    """
    chat_id: str
    message: str
