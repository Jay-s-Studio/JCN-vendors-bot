"""
Container
"""
from dependency_injector import containers, providers
from telegram import Bot

from app.config import settings
from app.handlers import TelegramBotMessagesHandler, TelegramMessagesHandler
from app.libs.database import RedisPool
from app.providers import ExchaigeAssistantProvider


# pylint: disable=too-few-public-methods,c-extension-no-member
class Container(containers.DeclarativeContainer):
    """Container"""

    wiring_config = containers.WiringConfiguration(
        modules=[],
        packages=["app.bots", "app.handlers", "app.routers"],
    )

    # [bot]
    bot = providers.Resource(
        Bot,
        token=settings.TELEGRAM_BOT_TOKEN
    )

    # [database]
    redis_pool = providers.Singleton(RedisPool)

    # [providers]
    exchaige_assistant_provider = providers.Factory(ExchaigeAssistantProvider)

    # [handlers]
    telegram_bot_messages_handler = providers.Factory(
        TelegramBotMessagesHandler,
        redis=redis_pool,
        exchaige_assistant_provider=exchaige_assistant_provider
    )
    telegram_messages_handler = providers.Factory(
        TelegramMessagesHandler,
        bot=bot,
        exchaige_assistant_provider=exchaige_assistant_provider
    )
