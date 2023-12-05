"""
Telegram bot application
"""
import telegram
from telegram.ext import ContextTypes, Application, CommandHandler, MessageHandler, filters

from app.config import settings
from app.context import CustomContext
from app.handlers.bot_handler import start, help_command, echo

__all__ = ["application", "bot"]

_context_types = ContextTypes(context=CustomContext)

bot = telegram.Bot(token=settings.TELEGRAM_BOT_TOKEN)
application = (
    Application.builder().token(settings.TELEGRAM_BOT_TOKEN).updater(None).context_types(_context_types).build()
)

# register handlers
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_command))
application.add_handler(MessageHandler(filters=filters.TEXT & ~filters.COMMAND, callback=echo))
