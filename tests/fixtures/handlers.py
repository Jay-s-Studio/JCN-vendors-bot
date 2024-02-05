"""
Fixtures for handlers
"""
import pytest

from app.handlers import (
    TelegramMessagesHandler
)
from app.containers import Container


@pytest.fixture
def telegram_messages_handler() -> TelegramMessagesHandler:
    """
    TelegramMessagesHandler
    :return:
    """
    return Container.telegram_messages_handler()
