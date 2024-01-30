"""
ExchaigeAssistantProvider
"""
from typing import List

from app.clients.exchaige_assistant import ExchaigeAssistantClient
from app.schemas.account.telegram import TelegramAccount, TelegramChatGroup
from app.schemas.exchaige_assistant import TelegramGroup


class ExchaigeAssistantProvider:
    """ExchaigeAssistantProvider"""

    def __init__(self):
        self.client = ExchaigeAssistantClient()

    async def set_account(self, account: TelegramAccount) -> None:
        """
        set account
        :param account:
        :return:
        """
        await self.client.telegram_account.set_account(
            data=account.model_dump(
                exclude={"updated_at"},
                exclude_none=True
            )
        )

    async def set_group(self, group: TelegramChatGroup) -> None:
        """
        set group
        :param group:
        :return:
        """
        await self.client.telegram_account.set_group(
            data=group.model_dump(
                exclude={"updated_at"},
                exclude_none=True
            )
        )

    async def init_chat_group_member(self, data: dict) -> None:
        """
        Initialize chat group member
        :param data:
        :return:
        """
        await self.client.telegram_account.init_chat_group_member(data=data)

    async def delete_chat_group_member(self, account_id: int, group_id: int) -> None:
        """
        delete chat group member
        :param account_id:
        :param group_id:
        :return:
        """
        data = {
            "account_id": account_id,
            "group_id": group_id
        }
        await self.client.telegram_account.delete_chat_group_member(data=data)

    async def get_vendors(self) -> List[TelegramGroup]:
        """
        get vendors
        :return:
        """
        result = await self.client.telegram_account.get_vendors()
        return [TelegramGroup(**vendor) for vendor in result.get("vendors")]
