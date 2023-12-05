"""
Configuration
"""
import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Configuration(BaseSettings):
    """
    Configuration
    """
    # [App Base]
    APP_NAME: str = "tg_bot_tutorial"
    ENV: str = os.getenv(key="ENV", default="dev").lower()
    DEBUG: bool = os.getenv(key="DEBUG", default=False)
    IS_PROD: bool = ENV == "prod"
    APP_FQDN: str = os.getenv(key="APP_FQDN", default="localhost")
    BASE_URL: str = f"https://{APP_FQDN}"

    # [Telegram]
    TELEGRAM_BOT_TOKEN: str = os.getenv(key="TELEGRAM_BOT_TOKEN")

    # [Sentry]
    SENTRY_URL: str = os.getenv(key="SENTRY_URL")


settings: Configuration = Configuration()
