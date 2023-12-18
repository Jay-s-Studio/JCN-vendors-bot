"""
ExchaigeAssistantClient
"""
from urllib.parse import urljoin

from httpx import HTTPStatusError

from app.config import settings
from app.libs.http_client import http_client


class ExchaigeAssistantClient:
    """ExchaigeAssistantClient"""

    def __init__(self):
        self.base_url = settings.JCN_EXCHAIGE_ASSISTANT_URL
        self._api_version = "/api/v1"

    async def get_currencies(self):
        """
        get a currency list
        :return:
        """
        url = urljoin(base=self.base_url, url=f"{self._api_version}/currency/all")
        resp = await http_client.create(url=url).aget()
        return resp.json()

    async def update_exchange_rate(self, payload: dict):
        """
        Update exchange rate
        :param payload:
        :return:
        """
        url = urljoin(base=self.base_url, url=f"{self._api_version}/exchange_rate/currency_rate")
        try:
            resp = await (
                http_client.create(url=url)
                .add_json(payload)
                .apost()
            )
            resp.raise_for_status()
        except HTTPStatusError as e:
            raise e
