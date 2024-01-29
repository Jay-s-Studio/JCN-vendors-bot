"""
Models for Telegram account
"""
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from app.libs.consts.enums import BotType


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
    created_at: Optional[datetime] = Field(default=None, description="Created At")
    created_by: Optional[str] = Field(default=None, description="Created By")
    created_by_id: Optional[UUID] = Field(default=None, description="Created By ID")
    updated_at: Optional[datetime] = Field(default=datetime.utcnow(), description="Updated At")
    updated_by: Optional[str] = Field(default=None, description="Updated By")
    updated_by_id: Optional[UUID] = Field(default=None, description="Updated By ID")
    delete_reason: Optional[str] = Field(default=None, description="Delete Reason")
    is_deleted: bool = Field(default=False, description="Is Deleted")
    description: Optional[str] = Field(default=None, description="Description")


class TelegramChatGroup(BaseModel):
    """TelegramChatGroup"""
    # telegram raw data
    id: int
    title: str
    type: str
    in_group: bool
    bot_type: BotType
    created_at: Optional[datetime] = Field(default=None, description="Created At")
    created_by: Optional[str] = Field(default=None, description="Created By")
    created_by_id: Optional[UUID] = Field(default=None, description="Created By ID")
    updated_at: Optional[datetime] = Field(default=datetime.utcnow(), description="Updated At")
    updated_by: Optional[str] = Field(default=None, description="Updated By")
    updated_by_id: Optional[UUID] = Field(default=None, description="Updated By ID")
    delete_reason: Optional[str] = Field(default=None, description="Delete Reason")
    is_deleted: bool = Field(default=False, description="Is Deleted")
    description: Optional[str] = Field(default=None, description="Description")
