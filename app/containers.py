"""
Container
"""
from dependency_injector import containers, providers
from telegram import Bot

from app.libs.database import RedisPool
from app.providers import TelegramAccountProvider
from app.handlers.telegram_bot import TelegramBotMessagesHandler
from app.handlers.telegram import TelegramHandler
from app.config import settings


# pylint: disable=too-few-public-methods,c-extension-no-member
class Container(containers.DeclarativeContainer):
    """Container"""

    wiring_config = containers.WiringConfiguration(
        modules=[],
        packages=["app.handlers", "app.routers"],
    )

    # [bot]
    bot = providers.Resource(
        Bot,
        token=settings.TELEGRAM_BOT_TOKEN
    )

    # [database]
    redis_pool = providers.Singleton(RedisPool)

    # [providers]
    telegram_account_provider = providers.Factory(
        TelegramAccountProvider,
        redis=redis_pool
    )

    # [handlers]
    telegram_bot_messages_handler = providers.Factory(
        TelegramBotMessagesHandler,
        redis=redis_pool,
        telegram_account_provider=telegram_account_provider
    )
    telegram_handler = providers.Factory(
        TelegramHandler,
        bot=bot,
        telegram_account_provider=telegram_account_provider
    )
