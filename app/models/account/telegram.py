"""
Models for Telegram account
"""
from typing import Optional

from pydantic import BaseModel

from app.libs.consts.enums import BotType


class CustomAccountInfo(BaseModel):
    """CustomAccountInfo"""
    description: Optional[str] = None


class TelegramAccount(BaseModel):
    """TelegramAccount"""
    id: int
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    full_name: Optional[str] = None
    name: Optional[str] = None
    language_code: Optional[str] = None
    is_bot: bool
    is_premium: bool = False
    link: Optional[str] = None
    custom_info: Optional[CustomAccountInfo] = None


class CustomGroupInfo(BaseModel):
    """CustomGroupInfo"""
    in_group: bool
    bot_type: BotType
    description: Optional[str] = None


class TelegramChatGroup(BaseModel):
    """TelegramChatGroup"""
    # telegram raw data
    id: int
    title: str
    type: str
    # custom fields
    custom_info: Optional[CustomGroupInfo] = None
