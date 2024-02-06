"""
ExchaigeAssistantTelegramMessages
"""
from httpx import HTTPStatusError

from app.libs.decorators.sentry_tracer import distributed_trace
from app.libs.http_client import http_client
from .base import ExchaigeAssistantBase


class ExchaigeAssistantTelegramMessages(ExchaigeAssistantBase):
    """ExchaigeAssistantTelegramMessages"""

    def __init__(self, url: str, headers: dict):
        super().__init__(url, headers)
        self._resource = "telegram/messages"

    @distributed_trace()
    async def send_payment_account(self, data: dict):
        """
        send the payment account
        :param data:
        :return:
        """
        url = self._get_resource_url(resource=self._resource, path="/payment_account")
        try:
            resp = await http_client.create(url=url) \
                .add_headers(self._headers) \
                .add_json(data) \
                .apost()
            resp.raise_for_status()
        except HTTPStatusError as exc:
            raise exc

    @distributed_trace()
    async def payment_account_out_of_stock(self, group_id: int, data: dict):
        """
        payment account out of stock
        :param group_id:
        :param data:
        :return:
        """
        url = self._get_resource_url(resource=self._resource, path=f"/payment_account_status/{group_id}")
        try:
            resp = await http_client.create(url=url) \
                .add_headers(self._headers) \
                .add_json(data) \
                .aput()
            resp.raise_for_status()
        except HTTPStatusError as exc:
            raise exc

    @distributed_trace()
    async def confirm_pay(self, data: dict):
        """
        confirm pay
        :param data:
        :return:
        """
        url = self._get_resource_url(resource=self._resource, path="/confirm_pay")
        try:
            resp = await http_client.create(url=url) \
                .add_headers(self._headers) \
                .add_json(data) \
                .apost()
            resp.raise_for_status()
        except HTTPStatusError as exc:
            raise exc
