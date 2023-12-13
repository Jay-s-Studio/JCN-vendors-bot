"""
Test currency provider
"""
import pytest

from app.libs.consts.enums import BotType
from app.providers import TelegramAccountProvider


@pytest.mark.asyncio
async def test_get_all_chat_group(telegram_account_provider: TelegramAccountProvider):
    """
    test get chat group
    :param telegram_account_provider:
    :return:
    """
    chat_groups = await telegram_account_provider.get_all_chat_group()
    assert chat_groups is not None


@pytest.mark.asyncio
async def test_get_chat_groups_by_bot_type(telegram_account_provider: TelegramAccountProvider):
    """
    test get chat group
    :param telegram_account_provider:
    :return:
    """
    chat_groups = await telegram_account_provider.get_chat_groups_by_bot_type(bot_type=BotType.VENDORS)
    assert chat_groups is not None
