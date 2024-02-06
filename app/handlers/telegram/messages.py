"""
TelegramMessagesHandler
"""
import telegram
from fastapi import HTTPException
from starlette import status
from telegram import Bot, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.constants import ParseMode

from app.libs.consts.enums import BotType
from app.libs.consts.messages import PaymentAccountMessage, ExchangeRateMessage, HurryPaymentAccountMessage
from app.libs.logger import logger
from app.providers import ExchaigeAssistantProvider
from app.serializers.v1.telegram import PaymentAccount, CheckReceipt


class TelegramMessagesHandler:
    """TelegramMessagesHandler"""

    def __init__(
        self,
        bot: Bot,
        exchaige_assistant_provider: ExchaigeAssistantProvider
    ):
        self._bot = bot
        self._exchaige_assistant_provider = exchaige_assistant_provider

    async def exchange_rate_msg(self):
        """
        exchange rate msg
        :return:
        """
        vendors = await self._exchaige_assistant_provider.get_vendors()
        message = ExchangeRateMessage.format()
        buttons = InlineKeyboardMarkup([(InlineKeyboardButton("Provide", callback_data="EXCHANGE_RATE provide"),)])
        for vendor in vendors:
            try:
                await self._bot.send_message(
                    chat_id=vendor.id,
                    text=message.text,
                    parse_mode=message.parse_mode,
                    reply_markup=buttons
                )
            except telegram.error.BadRequest as e:
                logger.error(e)
                continue

    async def payment_account(self, model: PaymentAccount):
        """
        payment telegram
        receive
        :param model:
        :return:
        """
        message = PaymentAccountMessage.format(
            total_amount=model.total_amount,
            payment_currency=model.payment_currency,
            exchange_currency=model.exchange_currency
        )
        buttons = InlineKeyboardMarkup(
            [
                (
                    InlineKeyboardButton(
                        text="Provide",
                        callback_data=f"PROVIDE_PA {model.customer_id} {model.session_id}"
                    ),
                    InlineKeyboardButton(
                        text="Out of stock",
                        callback_data=f"OUT_OF_STOCK {model.customer_id} {model.session_id}"
                    ),
                )
            ]
        )
        try:
            resp_message = await self._bot.send_message(
                chat_id=model.group_id,
                text=message.text,
                parse_mode=message.parse_mode,
                reply_markup=buttons
            )
        except telegram.error.BadRequest as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        return resp_message.to_dict()

    async def hurry_payment_account(self, model: PaymentAccount):
        """
        hurry the payment account
        :param model:
        :return:
        """
        message = HurryPaymentAccountMessage.format(
            total_amount=model.total_amount,
            payment_currency=model.payment_currency,
            exchange_currency=model.exchange_currency
        )
        buttons = InlineKeyboardMarkup(
            [
                (
                    InlineKeyboardButton(
                        text="Provide",
                        callback_data=f"PROVIDE_PA {model.customer_id} {model.session_id}"
                    ),
                    InlineKeyboardButton(
                        text="Out of stock",
                        callback_data=f"OUT_OF_STOCK {model.customer_id} {model.session_id}"
                    ),
                )
            ]
        )
        try:
            resp_message = await self._bot.send_message(
                chat_id=model.group_id,
                text=message.text,
                parse_mode=message.parse_mode,
                reply_markup=buttons
            )
        except telegram.error.BadRequest as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        return resp_message.to_dict()

    async def check_receipt(self, model: CheckReceipt):
        """
        send receipt
        :param model:
        :return:
        """
        try:
            file_content = await self._exchaige_assistant_provider.get_file(file_id=model.file_id, file_name=model.file_name)
            buttons = InlineKeyboardMarkup(
                [
                    (
                        InlineKeyboardButton(
                            text="Confirm payment",
                            callback_data=f"CONFIRM_PAY {model.customer_id} {model.session_id}"
                        ),
                    )
                ]
            )
            resp_message = await self._bot.send_photo(
                chat_id=model.group_id,
                photo=file_content,
                reply_markup=buttons
            )
        except telegram.error.BadRequest as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        return resp_message.to_dict()
