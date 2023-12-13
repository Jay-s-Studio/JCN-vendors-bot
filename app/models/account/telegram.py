"""
Models for Telegram account
"""
from typing import Optional

from pydantic import BaseModel

from app.libs.consts.enums import BotType


class TelegramAccount(BaseModel):
    """TelegramAccount"""
    id: int
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    language_code: Optional[str] = None
    is_bot: bool
    is_premium: bool = False


class TelegramChatGroup(BaseModel):
    """TelegramChatGroup"""
    id: int
    title: str
    type: str
    all_members_are_administrators: Optional[bool] = False
    bot_type: BotType
    in_group: bool
