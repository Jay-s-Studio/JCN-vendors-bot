"""
Configuration
"""
import json
import os

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
    APP_FQDN: str = os.getenv(key="APP_FQDN", default="localhost")
    BASE_URL: str = f"https://{APP_FQDN}"

    # [FastAPI]
    HOST: str = os.getenv(key="HOST", default="127.0.0.1")
    PORT: int = os.getenv(key="PORT", default=8000)

    # [JCN]
    JCN_EXCHAIGE_ASSISTANT_URL: str = os.getenv(key="JCN_EXCHAIGE_ASSISTANT_URL")

    # [Redis]
    REDIS_HOST: str = os.getenv(key="REDIS_HOST", default="localhost")
    REDIS_PORT: int = os.getenv(key="REDIS_PORT", default=6379)
    REDIS_USERNAME: str = os.getenv(key="REDIS_USERNAME")
    REDIS_PASSWORD: str = os.getenv(key="REDIS_PASSWORD")
    REDIS_SSL: bool = os.getenv(key="REDIS_SSL", default=True)

    # [Telegram]
    TELEGRAM_BOT_USERNAME: str = os.getenv(key="TELEGRAM_BOT_USERNAME")
    TELEGRAM_BOT_TOKEN: str = os.getenv(key="TELEGRAM_BOT_TOKEN")
    TELEGRAM_BOT_TYPE: BotType = BotType.VENDORS

    # [Sentry]
    SENTRY_URL: str = os.getenv(key="SENTRY_URL")

    # [Google Cloud]
    GOOGLE_FIREBASE_CERTIFICATE: dict = json.loads(os.getenv(key="GOOGLE_FIREBASE_CERTIFICATE"))


settings: Configuration = Configuration()
