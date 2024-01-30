"""
ExchaigeAssistantExchangeRate
"""
from httpx import HTTPStatusError

from app.libs.http_client import http_client
from .base import ExchaigeAssistantBase
from ...libs.decorators.sentry_tracer import distributed_trace


class ExchaigeAssistantExchangeRate(ExchaigeAssistantBase):
    """ExchaigeAssistantExchangeRate"""

    def __init__(self, url: str, headers: dict):
        super().__init__(url, headers)
        self._resource = "exchange_rate"

    @distributed_trace()
    async def update_exchange_rate(self, data: dict):
        """
        update exchange rate
        :return:
        """
        url = self._get_resource_url(resource=self._resource, path="/currency_rate")
        try:
            resp = await http_client.create(url=url) \
                .add_headers(self._headers) \
                .add_json(data) \
                .apost()
            resp.raise_for_status()
        except HTTPStatusError as exc:
            raise exc
