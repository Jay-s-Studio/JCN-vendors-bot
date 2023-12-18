"""
ExchaigeAssistantProvider
"""
from app.clients.exchaige_assistant import ExchaigeAssistantClient
from app.models.currency import Currencies


class ExchaigeAssistantProvider:
    """ExchaigeAssistantProvider"""

    def __init__(self):
        self.client = ExchaigeAssistantClient()

    async def get_currencies(self):
        """
        get currencies
        :return:
        """
        currencies = await self.client.get_currencies()
        return Currencies(**currencies)

    async def update_exchange_rate(self, group_id: str, currency_rates: list):
        """
        Update exchange rate
        :return:
        """
        data = {
            "group_id": group_id,
            "currency_rates": currency_rates
        }
        return await self.client.update_exchange_rate(payload=data)
