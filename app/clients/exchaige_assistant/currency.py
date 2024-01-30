"""
ExchaigeAssistantCurrency
"""
from httpx import HTTPStatusError

from app.libs.http_client import http_client
from .base import ExchaigeAssistantBase
from ...libs.decorators.sentry_tracer import distributed_trace


class ExchaigeAssistantCurrency(ExchaigeAssistantBase):
    """ExchaigeAssistantCurrency"""

    def __init__(self, url: str, headers: dict):
        super().__init__(url, headers)
        self._resource = "currency"

    @distributed_trace()
    async def get_currencies(self):
        """
        get currencies
        :return:
        """
        url = self._get_resource_url(resource=self._resource, path="/all")
        try:
            resp = await http_client.create(url=url) \
                .add_headers(self._headers) \
                .aget()
            resp.raise_for_status()
            return resp.json()
        except HTTPStatusError as exc:
            raise exc
