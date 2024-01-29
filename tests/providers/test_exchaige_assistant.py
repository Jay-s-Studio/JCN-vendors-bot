"""
Test Exchange Assistant provider
"""
import pytest

from app.models.currency import Currencies
from app.providers import ExchaigeAssistantProvider


@pytest.mark.asyncio
async def test_get_currency_list(exchaige_assistant_provider: ExchaigeAssistantProvider):
    """
    Test get a currency list
    :return:
    """
    # result = await exchaige_assistant_provider.get_currencies()
    # assert isinstance(result, Currencies)
