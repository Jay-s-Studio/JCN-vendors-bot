"""
Models for Telegram account
"""
from enum import Enum
from typing import Optional, Type

from pydantic import BaseModel, Field, field_serializer

from app.libs.consts.enums import BotType, PaymentAccountStatus


class TelegramAccount(BaseModel):
    """TelegramAccount"""
    id: int
    username: Optional[str] = Field(default=None, description="Username")
    first_name: Optional[str] = Field(default=None, description="First Name")
    last_name: Optional[str] = Field(default=None, description="Last Name")
    full_name: Optional[str] = Field(default=None, description="Full Name")
    name: Optional[str] = Field(default=None, description="Name")
    language_code: Optional[str] = Field(default=None, description="Language Code")
    is_bot: bool = Field(default=False, description="Is Bot")
    is_premium: bool = False
    link: Optional[str] = Field(default=None, description="Link")


class TelegramChatGroup(BaseModel):
    """TelegramChatGroup"""
    # telegram raw data
    id: int
    title: str
    type: str
    in_group: bool
    bot_type: BotType
    payment_account_status: Optional[PaymentAccountStatus] = Field(default=None, description="Payment Account Status")

    @field_serializer("bot_type", "payment_account_status")
    def serialize_enum(self, value: Type[Enum], _info):
        """
        serialize enum
        :param value:
        :param _info:
        :return:
        """
        return value.value
