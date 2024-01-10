"""
Telegram bot application
"""
from telegram import BotCommandScopeAllGroupChats, BotCommand, Bot
from telegram.ext import ContextTypes, Application, CommandHandler, MessageHandler, filters, ChatMemberHandler, CallbackQueryHandler

from app.config import settings
from app.context import CustomContext
from app.bots import telegram_bot

__all__ = ["application"]

_context_types = ContextTypes(context=CustomContext)

COMMANDS = [
    BotCommand(command="start", description="Start the bot"),
]


async def post_init(tg_application: Application) -> None:
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
    Application.builder()
    .token(settings.TELEGRAM_BOT_TOKEN)
    .context_types(_context_types)
    .post_init(post_init)
    .build()
)

# register handlers
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
