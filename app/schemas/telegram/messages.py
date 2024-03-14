"""
Schema for Telegram messages
"""
from uuid import UUID

from pydantic import BaseModel, field_serializer


class PaymentAccountProcess(BaseModel):
    order_id: UUID
    customer_id: int
    message_id: int

    @field_serializer("order_id")
    def serialize_uuid(self, value: UUID, _info) -> str:
        """

        :param value:
        :param _info:
        :return:
        """
        return str(value)
