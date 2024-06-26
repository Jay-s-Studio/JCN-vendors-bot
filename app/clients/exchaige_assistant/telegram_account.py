"""
ExchaigeAssistantTelegramAccount
"""
from httpx import HTTPStatusError

from app.libs.http_client import http_client
from .base import ExchaigeAssistantBase


class ExchaigeAssistantTelegramAccount(ExchaigeAssistantBase):
    """ExchaigeAssistantTelegramAccount"""

    def __init__(self, url: str, headers: dict):
        super().__init__(url, headers)
        self._resource = "telegram/account"

    async def set_account(self, data: dict):
        """
        set account
        :param data:
        :return:
        """
        url = self._get_resource_url(resource=self._resource, path="/raw/account")
        try:
            resp = await http_client.create(url=url) \
                .add_headers(self._headers) \
                .add_json(data) \
                .apost()
            resp.raise_for_status()
        except HTTPStatusError as exc:
            raise exc

    async def set_group(self, data: dict):
        """
        set group
        :param data:
        :return:
        """
        url = self._get_resource_url(resource=self._resource, path="/raw/group")
        try:
            resp = await http_client.create(url=url) \
                .add_headers(self._headers) \
                .add_json(data) \
                .apost()
            resp.raise_for_status()
        except HTTPStatusError as exc:
            raise exc

    async def init_chat_group_member(self, data: dict):
        """
        Initialize chat group member
        :param data:
        :return:
        """
        url = self._get_resource_url(resource=self._resource, path="/init_chat_group_member")
        try:
            resp = await http_client.create(url=url) \
                .add_headers(self._headers) \
                .add_json(data) \
                .apost()
            resp.raise_for_status()
        except HTTPStatusError as exc:
            raise exc

    async def delete_chat_group_member(self, data: dict):
        """
        delete chat group member
        :param data:
        :return:
        """
        url = self._get_resource_url(resource=self._resource, path="/delete_chat_group_member")
        try:
            resp = await http_client.create(url=url) \
                .add_headers(self._headers) \
                .add_json(data) \
                .apost()
            resp.raise_for_status()
        except HTTPStatusError as exc:
            raise exc

    async def get_vendors(self):
        """
        get vendors
        :return:
        """
        url = self._get_resource_url(resource=self._resource, path="/vendors")
        try:
            resp = await http_client.create(url=url) \
                .add_headers(self._headers) \
                .aget()
            resp.raise_for_status()
            return resp.json()
        except HTTPStatusError as exc:
            raise exc
