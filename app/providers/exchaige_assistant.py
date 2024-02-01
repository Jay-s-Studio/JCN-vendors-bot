"""
ExchaigeAssistantProvider
"""
from typing import List

from app.clients.exchaige_assistant import ExchaigeAssistantClient
from app.libs.decorators.sentry_tracer import distributed_trace
from app.schemas.account.telegram import TelegramAccount, TelegramChatGroup
from app.schemas.currency import Currencies


class ExchaigeAssistantProvider:
    """ExchaigeAssistantProvider"""

    def __init__(self):
        self.client = ExchaigeAssistantClient()

    @distributed_trace()
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

    @distributed_trace()
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

    @distributed_trace()
    async def init_chat_group_member(self, data: dict) -> None:
        """
        Initialize chat group member
        :param data:
        :return:
        """
        await self.client.telegram_account.init_chat_group_member(data=data)

    @distributed_trace()
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

    @distributed_trace()
    async def get_vendors(self) -> List[TelegramChatGroup]:
        """
        get vendors
        :return:
        """
        result = await self.client.telegram_account.get_vendors()
        return [TelegramChatGroup(**vendor) for vendor in result.get("vendors")]

    @distributed_trace()
    async def get_currencies(self) -> Currencies:
        """
        get currencies
        :return:
        """
        result = await self.client.currency.get_currencies()
        return Currencies(**result)

    @distributed_trace()
    async def update_exchange_rate(self, group_id: int, currency_rates: list):
        """
        get exchange rate
        :param group_id:
        :param currency_rates:
        :return:
        """
        data = {
            "group_id": group_id,
            "currency_rates": currency_rates
        }
        await self.client.exchange_rate.update_exchange_rate(data=data)
