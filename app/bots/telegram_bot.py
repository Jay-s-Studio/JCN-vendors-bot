"""
This module contains the Telegram application handlers.
"""
from dependency_injector.wiring import inject, Provide
from telegram import Update

from app.containers import Container
from app.context import CustomContext
from app.handlers.telegram_bot import TelegramBotMessagesHandler
from app.libs.decorators.sentry_tracer import start_transaction

TRANSACTION_NAME = "Telegram Update Queue Task"


@inject
@start_transaction(name=TRANSACTION_NAME)
async def start(
    update: Update,
    context: CustomContext,
    telegram_bot_messages_handler: TelegramBotMessagesHandler = Provide[Container.telegram_bot_messages_handler]
) -> None:
    """
    Send a message when the command /start is issued.
    :param update:
    :param context:
    :param telegram_bot_messages_handler:
    :return:
    """
    pass
    # user = update.effective_user
    # payload_url = html.escape(urljoin(base=settings.BASE_URL, url=f"/submitpayload?user_id=<your user id>&payload=<payload>"))
    # healthcheck_url = html.escape(urljoin(base=settings.BASE_URL, url=f"/healthcheck"))
    # text = (
    #     f"Hi {user.mention_html()}!\n\n"
    #     f"To check if the app is still running, call <code>{healthcheck_url}</code>.\n\n"
    #     f"To post a custom update, call <code>{payload_url}</code>.\n\n"
    #     f"Your user id is <code>{user.id}</code>.\n\n"
    # )
    # await update.message.reply_html(text=text)


@inject
@start_transaction(name=TRANSACTION_NAME)
async def receive_message(
    update: Update,
    context: CustomContext,
    telegram_bot_messages_handler: TelegramBotMessagesHandler = Provide[Container.telegram_bot_messages_handler]
) -> None:
    """
    Echo the user message.
    :param update:
    :param context:
    :param telegram_bot_messages_handler:
    :return:
    """
    await telegram_bot_messages_handler.receive_message(update, context)


@inject
@start_transaction(name=TRANSACTION_NAME)
async def track_chats(
    update: Update,
    context: CustomContext,
    telegram_bot_messages_handler: TelegramBotMessagesHandler = Provide[Container.telegram_bot_messages_handler]
) -> None:
    """
    Tracks the chats the bot is in.
    :param update:
    :param context:
    :param telegram_bot_messages_handler:
    :return:
    """
    await telegram_bot_messages_handler.track_chats(update, context)


@inject
@start_transaction(name=TRANSACTION_NAME)
async def new_member_handler(
    update: Update,
    context: CustomContext,
    telegram_bot_messages_handler: TelegramBotMessagesHandler = Provide[Container.telegram_bot_messages_handler]
) -> None:
    """

    :param update:
    :param context:
    :param telegram_bot_messages_handler:
    :return:
    """
    await telegram_bot_messages_handler.new_member_handler(update, context)


@inject
@start_transaction(name=TRANSACTION_NAME)
async def left_member_handler(
    update: Update,
    context: CustomContext,
    telegram_bot_messages_handler: TelegramBotMessagesHandler = Provide[Container.telegram_bot_messages_handler]
) -> None:
    """

    :param update:
    :param context:
    :param telegram_bot_messages_handler:
    :return:
    """
    await telegram_bot_messages_handler.left_member_handler(update, context)


# [Flow] exchange rate process
@inject
@start_transaction(name=TRANSACTION_NAME)
async def provide_exchange_rate(
    update: Update,
    context: CustomContext,
    telegram_bot_messages_handler: TelegramBotMessagesHandler = Provide[Container.telegram_bot_messages_handler]
) -> None:
    """

    :param update:
    :param context:
    :param telegram_bot_messages_handler:
    :return:
    """
    await telegram_bot_messages_handler.provide_exchange_rate(update, context)


@inject
@start_transaction(name=TRANSACTION_NAME)
async def provide_payment_account(
    update: Update,
    context: CustomContext,
    telegram_bot_messages_handler: TelegramBotMessagesHandler = Provide[Container.telegram_bot_messages_handler]
) -> None:
    """

    :param update:
    :param context:
    :param telegram_bot_messages_handler:
    :return:
    """
    await telegram_bot_messages_handler.provide_payment_account(update, context)


@inject
@start_transaction(name=TRANSACTION_NAME)
async def payment_account_out_of_stock(
    update: Update,
    context: CustomContext,
    telegram_bot_messages_handler: TelegramBotMessagesHandler = Provide[Container.telegram_bot_messages_handler]
) -> None:
    """

    :param update:
    :param context:
    :param telegram_bot_messages_handler:
    :return:
    """
    await telegram_bot_messages_handler.payment_account_out_of_stock(update, context)


@inject
@start_transaction(name=TRANSACTION_NAME)
async def confirm_pay(
    update: Update,
    context: CustomContext,
    telegram_bot_messages_handler: TelegramBotMessagesHandler = Provide[Container.telegram_bot_messages_handler]
) -> None:
    """

    :param update:
    :param context:
    :param telegram_bot_messages_handler:
    :return:
    """
    await telegram_bot_messages_handler.confirm_pay(update, context)
