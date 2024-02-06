"""
ExchaigeAssistantFiles
"""
from httpx import HTTPStatusError

from app.libs.http_client import http_client
from .base import ExchaigeAssistantBase
from app.libs.decorators.sentry_tracer import distributed_trace


class ExchaigeAssistantFiles(ExchaigeAssistantBase):
    """ExchaigeAssistantCurrency"""

    def __init__(self, url: str, headers: dict):
        super().__init__(url, headers)
        self._resource = "files"

    @distributed_trace()
    async def get_file(self, file_id: str, file_name: str) -> bytes:
        """
        get currencies
        :return:
        """
        url = self._get_resource_url(resource=self._resource, path=f"/{file_id}/{file_name}")
        try:
            resp = await http_client.create(url=url) \
                .add_headers(self._headers) \
                .aget()
            resp.raise_for_status()
            return resp.content
        except HTTPStatusError as exc:
            raise exc
