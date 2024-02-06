"""
ExchaigeAssistantClient
"""
from app.config import settings
from .currency import ExchaigeAssistantCurrency
from .exchange_rate import ExchaigeAssistantExchangeRate
from .files import ExchaigeAssistantFiles
from .telegram_account import ExchaigeAssistantTelegramAccount
from .telegram_messages import ExchaigeAssistantTelegramMessages


class ExchaigeAssistantClient:
    """ExchaigeAssistantClient"""

    def __init__(self):
        self.base_url = settings.JCN_EXCHAIGE_ASSISTANT_URL
        self._headers = {
            "X-API-KEY": settings.JCN_EXCHAIGE_ASSISTANT_API_KEY
        }

    @property
    def currency(self) -> ExchaigeAssistantCurrency:
        """

        :return:
        """
        return ExchaigeAssistantCurrency(url=self.base_url, headers=self._headers)

    @property
    def exchange_rate(self) -> ExchaigeAssistantExchangeRate:
        """

        :return:
        """
        return ExchaigeAssistantExchangeRate(url=self.base_url, headers=self._headers)

    @property
    def files(self) -> ExchaigeAssistantFiles:
        """

        :return:
        """
        return ExchaigeAssistantFiles(url=self.base_url, headers=self._headers)

    @property
    def telegram_account(self) -> ExchaigeAssistantTelegramAccount:
        """

        :return:
        """
        return ExchaigeAssistantTelegramAccount(url=self.base_url, headers=self._headers)

    @property
    def telegram_messages(self) -> ExchaigeAssistantTelegramMessages:
        """

        :return:
        """
        return ExchaigeAssistantTelegramMessages(url=self.base_url, headers=self._headers)
