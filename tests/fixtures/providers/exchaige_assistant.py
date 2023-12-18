"""
Fixtures for Exchange Assistant
"""
import pytest

from app.providers import ExchaigeAssistantProvider
from app.containers import Container


@pytest.fixture
def exchaige_assistant_provider() -> ExchaigeAssistantProvider:
    """
    exchaige assistant provider
    :return:
    """
    return Container.exchaige_assistant_provider()
