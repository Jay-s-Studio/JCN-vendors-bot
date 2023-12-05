#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handlers functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the app is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
app.
"""
from urllib.parse import urljoin

import sentry_sdk
import uvicorn
from fastapi import FastAPI
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.httpx import HttpxIntegration
from starlette.requests import Request
from starlette.responses import Response
from telegram import Update

from app.routers import root_router
from .bot import application
from .config import settings

sentry_sdk.init(
    dsn=settings.SENTRY_URL,
    integrations=[
        FastApiIntegration(),
        HttpxIntegration(),
        # RedisIntegration(),
    ],
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
    environment=settings.ENV.upper(),
    enable_tracing=True,
)


def setup_routers(webapi_app: FastAPI):
    """

    :param webapi_app:
    :return:
    """
    webapi_app.include_router(router=root_router)


def setup_middlewares(webapi_app: FastAPI):
    """

    :param webapi_app:
    :return:
    """


async def run_application():
    """
    Run the application
    :return:
    """
    telegram_webhook_path = "/webhooks/v1/telegram"

    # Pass webhook settings to telegram
    await application.bot.set_webhook(
        url=urljoin(base=settings.BASE_URL, url=telegram_webhook_path),
        allowed_updates=Update.ALL_TYPES,
        pool_timeout=5
    )

    # Set up webserver
    async def telegram(request: Request) -> Response:
        """Handle incoming Telegram updates by putting them into the `update_queue`"""
        update = Update.de_json(data=await request.json(), bot=application.bot)
        await application.update_queue.put(update)
        return Response()

    webapi_app = FastAPI()
    webapi_app.add_route(path=telegram_webhook_path, route=telegram, methods=["POST"], name="telegram webhook")
    setup_routers(webapi_app)

    webserver = uvicorn.Server(
        config=uvicorn.Config(
            app=webapi_app,
            host="127.0.0.1" if settings.DEBUG else "0.0.0.0"
        )
    )

    # Run application and webserver together
    async with application:
        await application.start()
        await webserver.serve()
        await application.stop()
