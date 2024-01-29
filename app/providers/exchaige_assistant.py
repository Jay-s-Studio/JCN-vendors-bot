"""
ExchaigeAssistantProvider
"""
from app.clients.exchaige_assistant import ExchaigeAssistantClient
from app.schemas.account.telegram import TelegramAccount, TelegramChatGroup


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
        await self.client.telegram_account.set_account(data=account.model_dump())

    async def set_group(self, group: TelegramChatGroup) -> None:
        """
        set group
        :param group:
        :return:
        """
        await self.client.telegram_account.set_group(data=group.model_dump())

    async def update_account_group_relation(self, account_id: int, group_id: int) -> None:
        """
        update account group relation
        :param account_id:
        :param group_id:
        :return:
        """
        data = {
            "account_id": account_id,
            "group_id": group_id
        }
        await self.client.telegram_account.update_account_group_relation(data=data)
