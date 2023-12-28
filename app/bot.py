"""
Telegram bot application
"""
from telegram.ext import ContextTypes, Application, CommandHandler, MessageHandler, filters, ChatMemberHandler, CallbackQueryHandler

from app.config import settings
from app.context import CustomContext
from app.bots import telegram_bot

__all__ = ["application"]

_context_types = ContextTypes(context=CustomContext)

application = (
    Application.builder()
    .token(settings.TELEGRAM_BOT_TOKEN)
    .context_types(_context_types)
    .build()
)

# register handlers
application.add_handler(CommandHandler(
    command="start",
    callback=telegram_bot.start
))
# Keep track of which chats the bot is in
application.add_handler(ChatMemberHandler(callback=telegram_bot.track_chats))

# Handle members joining/leaving chats.
application.add_handler(MessageHandler(
    filters=filters.StatusUpdate.NEW_CHAT_MEMBERS,
    callback=telegram_bot.new_member_handler
))

application.add_handler(MessageHandler(
    filters=filters.TEXT & filters.UpdateType.MESSAGES & ~filters.COMMAND,
    callback=telegram_bot.receive_message
))

# Exchange rates
application.add_handler(CallbackQueryHandler(
    callback=telegram_bot.provide_exchange_rate,
    pattern="^EXCHANGE_RATE"
))
