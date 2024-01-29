"""
Test Exchange Assistant provider
"""
import pytest

from app.providers import ExchaigeAssistantProvider


@pytest.mark.asyncio
async def test_get_vendors(exchaige_assistant_provider: ExchaigeAssistantProvider):
    """
    Test get a currency list
    :return:
    """
    result = await exchaige_assistant_provider.get_vendors()
    assert result is not None
