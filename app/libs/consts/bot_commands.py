"""
Command constants for bot
"""
from telegram import BotCommand

PROVIDE_EXCHANGE_RATE = BotCommand(command="provide_exchange_rate", description="Provide exchange rate")
PAYMENT_ACCOUNT_STATUS = BotCommand(command="payment_account_status", description="Update payment account status")


COMMANDS = [
    PROVIDE_EXCHANGE_RATE,
    PAYMENT_ACCOUNT_STATUS
]
