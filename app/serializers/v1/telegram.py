"""
Serializers for Telegram API
"""
from uuid import UUID

from pydantic import BaseModel


class PaymentAccount(BaseModel):
    """
    Telegram Flow Chat
    """
    session_id: UUID
    customer_id: int
    group_id: int
    payment_currency: str
    exchange_currency: str
    total_amount: float


class CheckReceipt(BaseModel):
    """
    Check Receipt
    """
    session_id: UUID
    customer_id: int
    group_id: int
    file_id: str
    file_name: str
