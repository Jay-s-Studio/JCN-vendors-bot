"""
Command constants for bot
"""
from telegram import BotCommand

PROVIDE_EXCHANGE_RATE = BotCommand(command="provide_exchange_rate", description="Provide exchange rate")


COMMANDS = [
    PROVIDE_EXCHANGE_RATE,
]
