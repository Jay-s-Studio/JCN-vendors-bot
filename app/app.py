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
import asyncio
from urllib.parse import urljoin

import sentry_sdk
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.exception_handlers import http_exception_handler
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.httpx import HttpxIntegration
from starlette.requests import Request
from starlette.responses import Response
from telegram import Update

from app.routers import api_router, webhook_router
from .bot import application, setup_commands
from .config import settings
from .containers import Container

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

TELEGRAM_WEBHOOK_PATH = "/webhook/v1/telegram"


def setup_routers(fastapi_app: FastAPI):
    """

    :param fastapi_app:
    :return:
    """
    fastapi_app.include_router(router=api_router, prefix="/api")
    fastapi_app.include_router(router=webhook_router, prefix="/webhook")


def setup_middlewares(webapi_app: FastAPI):
    """

    :param webapi_app:
    :return:
    """
    # webapi_app.add_middleware(
    #     CORSMiddleware,
    #     allow_origins=settings.CORS_ALLOWED_ORIGINS,
    #     allow_credentials=True,
    #     allow_methods=["*"],
    #     allow_headers=["*"],
    #     allow_origin_regex=settings.CORS_ALLOW_ORIGINS_REGEX
    # )


def get_application() -> FastAPI:
    """
    Get application
    :return:
    """
    fastapi_app = FastAPI()
    if not settings.IS_DEV:
        fastapi_app = FastAPI(
            docs_url="/swagger/api/documents",
            openapi_url="/open_api/documents/openapi.json",
            redoc_url=None,
        )
    # set container
    container = Container()
    fastapi_app.container = container

    setup_routers(fastapi_app)
    # setup_middlewares(fastapi_app)

    return fastapi_app


async def run_application():
    """
    Run the application
    :return:
    """
    await setup_commands(application)

    # Pass webhook settings to telegram
    await application.bot.set_webhook(
        url=urljoin(base=settings.BASE_URL, url=TELEGRAM_WEBHOOK_PATH),
        allowed_updates=Update.ALL_TYPES,
        pool_timeout=5
    )

    web_application = get_application()

    @web_application.middleware("http")
    async def http_middleware_handler(request: Request, callback):
        """

        :param request:
        :param callback:
        :return:
        """
        try:
            response: Response = await callback(request)
            if not settings.IS_DEV:
                await asyncio.sleep(1.5)
            return response
        finally:
            container: Container = request.app.container
            container.reset_singletons()

    @web_application.exception_handler(HTTPException)
    async def root_http_exception_handler(request, exc: HTTPException):
        """

        :param request:
        :param exc:
        :return:
        """
        return await http_exception_handler(request, exc)

    webserver = uvicorn.Server(
        config=uvicorn.Config(
            app=web_application,
            host=settings.HOST,
            port=settings.PORT
        )
    )

    # Run application and webserver together
    async with application:
        await application.start()
        await webserver.serve()
        await application.stop()
