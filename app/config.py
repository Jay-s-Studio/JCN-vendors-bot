"""
Configuration
"""
import json
import os
from pathlib import Path, PosixPath

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

from app.libs.consts.enums import BotType

load_dotenv()


class Configuration(BaseSettings):
    """
    Configuration
    """
    # [App Base]
    APP_NAME: str = "jcn_exchaige_assistant"
    ENV: str = os.getenv(key="ENV", default="dev").lower()
    DEBUG: bool = os.getenv(key="DEBUG", default=False)
    IS_PROD: bool = ENV == "prod"
    IS_DEV: bool = ENV not in ["prod", "stg"]
    APP_FQDN: str = os.getenv(key="APP_FQDN", default="localhost")
    BASE_URL: str = f"https://{APP_FQDN}"

    # [FastAPI]
    HOST: str = os.getenv(key="HOST", default="127.0.0.1")
    PORT: int = os.getenv(key="PORT", default=8000)

    # [JCN]
    JCN_EXCHAIGE_ASSISTANT_URL: str = os.getenv(key="JCN_EXCHAIGE_ASSISTANT_URL")
    JCN_EXCHAIGE_ASSISTANT_API_KEY: str = os.getenv(key="JCN_EXCHAIGE_ASSISTANT_API_KEY")

    # [Redis]
    REDIS_URL: str = os.getenv(key="REDIS_URL", default="redis://localhost:6379")

    # [Telegram]
    TELEGRAM_BOT_USERNAME: str = os.getenv(key="TELEGRAM_BOT_USERNAME")
    TELEGRAM_BOT_TOKEN: str = os.getenv(key="TELEGRAM_BOT_TOKEN")
    TELEGRAM_BOT_TYPE: BotType = BotType.VENDORS

    # [Sentry]
    SENTRY_URL: str = os.getenv(key="SENTRY_URL")


settings: Configuration = Configuration()
