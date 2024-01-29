"""
ExchaigeAssistantClient
"""
from app.config import settings
from .telegram_account import ExchaigeAssistantTelegramAccount


class ExchaigeAssistantClient:
    """ExchaigeAssistantClient"""

    def __init__(self):
        self.base_url = settings.JCN_EXCHAIGE_ASSISTANT_URL
        self._headers = {}

    @property
    def telegram_account(self) -> ExchaigeAssistantTelegramAccount:
        """

        :return:
        """
        return ExchaigeAssistantTelegramAccount(url=self.base_url, headers=self._headers)


