"""
Serializers for Telegram API
"""
from uuid import UUID

from pydantic import BaseModel


class PaymentAccount(BaseModel):
    """
    Telegram Flow Chat
    """
    order_id: UUID
    customer_id: int
    vendor_id: int
    payment_currency: str
    exchange_currency: str
    total_amount: float


class CheckReceipt(BaseModel):
    """
    Check Receipt
    """
    order_id: UUID
    customer_id: int
    vendor_id: int
    file_id: str
    file_name: str


class ConfirmPayment(BaseModel):
    """
    Confirm Payment
    """
    order_id: UUID
    customer_id: int
    vendor_id: int
    message_id: int
