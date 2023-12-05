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
import html
from urllib.parse import urljoin

from telegram import ForceReply, Update

from app.config import settings
from app.context import CustomContext


async def start(update: Update, context: CustomContext) -> None:
    """
    Send a message when the command /start is issued.
    :param update:
    :param context:
    :return:
    """
    user = update.effective_user
    payload_url = html.escape(urljoin(base=settings.BASE_URL, url=f"/submitpayload?user_id=<your user id>&payload=<payload>"))
    healthcheck_url = html.escape(urljoin(base=settings.BASE_URL, url=f"/healthcheck"))
    text = (
        f"Hi {user.mention_html()}!\n\n"
        f"To check if the app is still running, call <code>{healthcheck_url}</code>.\n\n"
        f"To post a custom update, call <code>{payload_url}</code>.\n\n"
        f"Your user id is <code>{user.id}</code>.\n\n"
    )
    await update.message.reply_html(
        text=text,
        # reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: CustomContext) -> None:
    """
    Send a message when the command /help is issued.
    :param update:
    :param context:
    :return:
    """
    await update.message.reply_text("Help!")


async def echo(update: Update, context: CustomContext) -> None:
    """
    Echo the user message.
    :param update:
    :param context:
    :return:
    """
    await update.message.reply_text(update.message.text)
