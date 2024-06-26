"""
ExchaigeAssistantProvider
"""
from typing import List
from uuid import UUID

from app.clients.exchaige_assistant import ExchaigeAssistantClient
from app.libs.consts.enums import PaymentAccountStatus
from app.libs.decorators.sentry_tracer import distributed_trace
from app.schemas.telegram.account import TelegramAccount, TelegramChatGroup
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
        await self.client.telegram_account.set_account(data=account.model_dump(exclude_none=True))

    @distributed_trace()
    async def set_group(self, group: TelegramChatGroup) -> None:
        """
        set group
        :param group:
        :return:
        """
        await self.client.telegram_account.set_group(data=group.model_dump())

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

    @distributed_trace()
    async def get_file(self, file_id: str, file_name: str) -> bytes:
        """
        get file
        :param file_id:
        :param file_name:
        :return:
        """
        return await self.client.files.get_file(file_id=file_id, file_name=file_name)

    @distributed_trace()
    async def update_payment_account_status(self, group_id: int, status: PaymentAccountStatus) -> None:
        """
        update payment account status
        :param group_id:
        :param status:
        :return:
        """
        data = {
            "status": status.value
        }
        await self.client.telegram_messages.update_payment_account_status(group_id=group_id, data=data)

    @distributed_trace()
    async def payment_account_out_of_stock(
        self,
        group_id: int,
        customer_id: int,
        order_id: UUID,
        status: PaymentAccountStatus
    ) -> None:
        """
        payment account out of stock
        :param group_id:
        :param customer_id:
        :param order_id:
        :param status:
        :return:
        """
        data = {
            "customer_id": customer_id,
            "order_id": str(order_id),
            "status": status.value
        }
        await self.client.telegram_messages.payment_account_out_of_stock(group_id=group_id, data=data)

    @distributed_trace()
    async def send_payment_account(
        self,
        message: str,
        message_id: int,
        customer_id: int,
        order_id: UUID
    ) -> None:
        """
        send the payment account
        :param message:
        :param message_id:
        :param customer_id:
        :param order_id:
        :return:
        """
        data = {
            "message": message,
            "message_id": message_id,
            "customer_id": customer_id,
            "order_id": str(order_id)
        }
        await self.client.telegram_messages.send_payment_account(data=data)

    @distributed_trace()
    async def confirm_pay(self, customer_id: int, order_id: UUID) -> None:
        """
        confirm pay
        :param customer_id:
        :param order_id:
        :return:
        """
        data = {
            "customer_id": customer_id,
            "order_id": str(order_id),
        }
        await self.client.telegram_messages.confirm_pay(data=data)
