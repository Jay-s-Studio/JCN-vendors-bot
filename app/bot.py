"""
Telegram bot application
"""
from telegram import BotCommandScopeAllGroupChats, Bot
from telegram.ext import (
    ContextTypes,
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ChatMemberHandler,
    CallbackQueryHandler,
    ApplicationBuilder,
)

from app.bots import telegram_bot
from app.config import settings
from app.context import CustomContext
from app.libs.consts.bot_commands import (
    COMMANDS,
    PROVIDE_EXCHANGE_RATE,
    PAYMENT_ACCOUNT_STATUS
)

__all__ = ["application"]

_context_types = ContextTypes(context=CustomContext)


async def setup_commands(tg_application: Application) -> None:
    """

    :param tg_application:
    :return:
    """
    bot: Bot = tg_application.bot
    # delete commands
    await bot.delete_my_commands(scope=BotCommandScopeAllGroupChats())
    # set commands
    await bot.set_my_commands(
        commands=COMMANDS,
        scope=BotCommandScopeAllGroupChats(),
    )


application = (
    ApplicationBuilder()
    .token(settings.TELEGRAM_BOT_TOKEN)
    .context_types(_context_types)
    .build()
)

# register handlers
if settings.IS_DEV:
    application.add_handler(
        CommandHandler(
            command="start",
            callback=telegram_bot.start
        )
    )
# Keep track of which chats the bot is in
application.add_handler(ChatMemberHandler(callback=telegram_bot.track_chats))

# Handle members joining/leaving chats.
application.add_handler(
    MessageHandler(
        filters=filters.StatusUpdate.NEW_CHAT_MEMBERS,
        callback=telegram_bot.new_member_handler
    )
)
application.add_handler(
    MessageHandler(
        filters=filters.StatusUpdate.LEFT_CHAT_MEMBER,
        callback=telegram_bot.left_member_handler
    )
)

application.add_handler(
    MessageHandler(
        filters=filters.TEXT & filters.UpdateType.MESSAGES & ~filters.COMMAND,
        callback=telegram_bot.receive_message
    )
)

# Exchange rates
application.add_handler(
    CallbackQueryHandler(
        callback=telegram_bot.provide_exchange_rate,
        pattern="^EXCHANGE_RATE"
    )
)
application.add_handler(
    CommandHandler(
        command=PROVIDE_EXCHANGE_RATE.command,
        callback=telegram_bot.provide_exchange_rate
    )
)

# Payment telegram
application.add_handler(
    CallbackQueryHandler(
        callback=telegram_bot.provide_payment_account,
        pattern="^PROVIDE_PA"
    )
)
application.add_handler(
    CallbackQueryHandler(
        callback=telegram_bot.payment_account_out_of_stock,
        pattern="^OUT_OF_STOCK"
    )
)
application.add_handler(
    CommandHandler(
        command=PAYMENT_ACCOUNT_STATUS.command,
        callback=telegram_bot.payment_account_status
    )
)
application.add_handler(
    CallbackQueryHandler(
        callback=telegram_bot.update_payment_account_status,
        pattern="^PA_STATUS"
    )
)

# Check receipt
application.add_handler(
    CallbackQueryHandler(
        callback=telegram_bot.confirm_pay,
        pattern="^CONFIRM_PAY"
    )
)
