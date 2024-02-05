"""
Test Telegram messages handler
"""
import uuid

import pytest

from app.handlers import TelegramMessagesHandler
from app.serializers.v1.telegram import PaymentAccount


@pytest.mark.asyncio
async def test_exchange_rate_msg(telegram_messages_handler: TelegramMessagesHandler):
    """
    Test exchange rate message
    """
    await telegram_messages_handler.exchange_rate_msg()


@pytest.mark.asyncio
async def test_payment_account(telegram_messages_handler: TelegramMessagesHandler):
    """
    Test payment account
    """
    model = PaymentAccount(
        session_id=uuid.uuid4(),
        group_id=-4100117630,
        total_amount=20 * 56.7,
        payment_currency="PHP",
        exchange_currency="GCASH",
    )
    await telegram_messages_handler.payment_account(model=model)
