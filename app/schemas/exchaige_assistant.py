"""
Schema for Exchange Assistant
"""
from typing import Optional

from pydantic import BaseModel, Field

from app.libs.consts.enums import BotType


class TelegramGroup(BaseModel):
    """
    Telegram Broadcast
    """
    id: int = Field(description="Group ID")
    title: str = Field(description="Group Title")
    description: Optional[str] = Field(default=None, description="Group Description")
    in_group: bool = Field(description="Is In Group")
    bot_type: BotType = Field(description="Group Bot Type")
