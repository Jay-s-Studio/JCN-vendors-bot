"""
Fixtures for account provider
"""
import pytest

from app.providers.account import TelegramAccountProvider
from app.containers import Container


@pytest.fixture
def telegram_account_provider() -> TelegramAccountProvider:
    """
    telegram account provider
    :return:
    """
    return Container.telegram_account_provider()
