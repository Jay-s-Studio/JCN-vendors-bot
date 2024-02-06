"""
TelegramBotMessagesHandler
"""
from typing import cast

from telegram import Update, ForceReply, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.constants import ParseMode

from app.config import settings
from app.context import CustomContext
from app.libs.consts.enums import PaymentAccountStatus
from app.libs.consts.messages import PaymentAccountStatusMessage
from app.libs.database import RedisPool
from app.libs.decorators.sentry_tracer import distributed_trace
from app.libs.logger import logger
from app.providers import ExchaigeAssistantProvider
from app.schemas.telegram.account import TelegramAccount, TelegramChatGroup
from app.schemas.telegram.messages import PaymentAccountProcess
from .base import TelegramBotBaseHandler


class TelegramBotMessagesHandler(TelegramBotBaseHandler):
    """TelegramBotMessagesHandler"""

    def __init__(
        self,
        redis: RedisPool,
        exchaige_assistant_provider: ExchaigeAssistantProvider
    ):
        super().__init__(
            redis=redis,
            exchaige_assistant_provider=exchaige_assistant_provider
        )
        self._exchaige_assistant_provider = exchaige_assistant_provider

    @staticmethod
    def redis_name(name: str):
        """

        :return:
        """
        return f"{settings.APP_NAME}:{name}"

    @distributed_trace()
    async def receive_message(self, update: Update, context: CustomContext) -> None:
        """
        receive message
        :param update:
        :param context:
        :return:
        """
        await self.setup_account_info(
            account=TelegramAccount(**update.effective_user.to_dict()),
            chat_group=TelegramChatGroup(
                **update.effective_chat.to_dict(),
                in_group=True,
                bot_type=settings.TELEGRAM_BOT_TYPE
            )
        )
        chat_id = update.effective_chat.id
        reply_message_id = update.effective_message.reply_to_message.message_id if update.effective_message.reply_to_message else None

        # [Flow] exchange rate process
        redis_name = self.redis_name(name=f"exchange_rate_process:{chat_id}")
        exchange_rate_process_message_id = await self._redis.get(redis_name)
        if exchange_rate_process_message_id and reply_message_id == exchange_rate_process_message_id:
            await self.parse_exchange_rate(update)
            return

        # [Flow] payment telegram process
        redis_name = self.redis_name(name=f"payment_account_process:{chat_id}")
        payment_account_process_value = await self._redis.get(redis_name)
        model = PaymentAccountProcess.model_validate_json(payment_account_process_value) if payment_account_process_value else None
        if payment_account_process_value and reply_message_id == model.message_id:
            await self.process_payment_account(update=update, model=model)
            return

    # --------------------------------------------------
    # [Flow] exchange rate process
    @distributed_trace()
    async def provide_exchange_rate(self, update: Update, context: CustomContext) -> None:
        """
        provide exchange rate
        :param update:
        :param context:
        :return:
        """
        text = (
            "Please _*reply*_ this message and follow this format to provide the exchange rate for USDT *\(in 1 hour\)* :\n"
            "`{currency}:{buy rate}|{sell rate}`\n"
            "Example 1:\n`USD:0.99|0.98,CAD:1.34|1.33,GCASH:56.8,PAYMAYA:56.8,BANK:56.7,PESO:56.4`\n"
            "Example 2:\n`USD:0.99|0.98`\n`GCASH:56.8`\n`PAYMAYA:56.8`\n`BANK:56.7`\n`PESO:56.4`"
        )
        message = await update.effective_chat.send_message(
            text=text,
            parse_mode=ParseMode.MARKDOWN_V2,
            reply_markup=ForceReply(selective=False)
        )
        redis_name = self.redis_name(name=f"exchange_rate_process:{update.effective_chat.id}")
        await self._redis.set(
            name=redis_name,
            value=message.message_id,
            ex=60 * 60  # 1 hour
        )

    @distributed_trace()
    async def parse_exchange_rate(self, update: Update):
        """

        :param update:
        :return:
        """
        message = update.effective_message.text
        if "," in message:
            exchange_rate_list = message.split(",")
        elif "\n" in message:
            exchange_rate_list = message.split("\n")
        else:
            exchange_rate_list = [message]
        currencies = await self._exchaige_assistant_provider.get_currencies()
        currency_symbol_mapping = {currency.symbol: currency.id for currency in currencies.currencies}
        errors = []
        currency_rates = []
        for exchange_rate in exchange_rate_list:
            try:
                currency, rates = exchange_rate.split(":")
                if currency not in currency_symbol_mapping.keys():
                    continue
                if "|" in rates:
                    buy_rate, sell_rate = rates.split("|")
                else:
                    buy_rate, sell_rate = rates, rates
                print(currency, buy_rate, sell_rate)
                if not currency or not buy_rate or not sell_rate:
                    errors.append(exchange_rate)
                    continue
                currency_rates.append(
                    {
                        "currency_id": str(currency_symbol_mapping.get(currency)),
                        "buy_rate": float(buy_rate),
                        "sell_rate": float(sell_rate)
                    }
                )
            except Exception as e:
                logger.exception(e)
                errors.append(exchange_rate)
                continue
        if errors:
            await update.effective_message.reply_text(
                text="Sorry, there are some incorrect formats:\n"
                     f"`{','.join(errors)}`\n"
                     "Please follow this format to provide the exchange rate for USDT: "
                     "`{currency}:{buy rate}|{sell rate}`",
                parse_mode=ParseMode.MARKDOWN_V2
            )
            return
        currency_ids = [currency_rate["currency_id"] for currency_rate in currency_rates]
        for currency_id in currency_symbol_mapping.values():
            currency_id = str(currency_id)
            if currency_id not in currency_ids:
                currency_rates.append(
                    {
                        "currency_id": currency_id,
                        "buy_rate": None,
                        "sell_rate": None
                    }
                )
        try:
            await self._exchaige_assistant_provider.update_exchange_rate(
                group_id=update.effective_chat.id,
                currency_rates=currency_rates
            )
        except Exception as e:
            logger.exception(e)
            await update.effective_message.reply_text(
                text="Sorry, something went wrong\. Please try again later\.",
                parse_mode=ParseMode.MARKDOWN_V2
            )
            return
        await update.effective_message.reply_text(text="Thank you for your cooperation.")
        # await self._redis.delete(self.redis_name(name=f"exchange_rate_process:{update.effective_chat.id}"))

    # --------------------------------------------------
    # [Flow] payment telegram process
    @distributed_trace()
    async def provide_payment_account(self, update: Update, context: CustomContext) -> None:
        """

        :param update:
        :param context:
        :return:
        """
        callback_query = update.callback_query
        _, customer_id, session_id = cast(str, callback_query.data).split()
        text = "Please _*reply*_ this message to provide the payment telegram"
        await update.effective_chat.send_chat_action("typing")
        edit_text = f"{update.effective_message.text_markdown_v2}\n\n(Selected *Provide*)"
        await update.effective_message.edit_text(
            text=edit_text,
            parse_mode=ParseMode.MARKDOWN_V2
        )
        message = await update.effective_chat.send_message(
            text=text,
            parse_mode=ParseMode.MARKDOWN_V2,
            reply_markup=ForceReply(selective=False)
        )
        value = PaymentAccountProcess(
            session_id=session_id,
            customer_id=int(customer_id),
            message_id=message.message_id
        )
        redis_name = self.redis_name(name=f"payment_account_process:{update.effective_chat.id}")
        await self._redis.set(
            name=redis_name,
            value=value.model_dump_json(),
            ex=60 * 60  # 1 hour
        )

    @distributed_trace()
    async def payment_account_out_of_stock(self, update: Update, context: CustomContext) -> None:
        """

        :param update:
        :param context:
        :return:
        """
        callback_query = update.callback_query
        _, customer_id, session_id = cast(str, callback_query.data).split()
        try:
            await self._exchaige_assistant_provider.payment_account_out_of_stock(
                group_id=update.effective_chat.id,
                customer_id=int(customer_id),
                session_id=session_id,
                status=PaymentAccountStatus.OUT_OF_STOCK
            )
            edit_text = f"{update.effective_message.text_markdown_v2}\n\n(Selected *Out of Stock*)"
            await update.effective_message.edit_text(
                text=edit_text,
                parse_mode=ParseMode.MARKDOWN_V2
            )
        except Exception as e:
            logger.exception(e)
            await update.effective_message.reply_text(
                text="Sorry, something went wrong\. Please try again later\.",
                parse_mode=ParseMode.MARKDOWN_V2
            )
            return

    @distributed_trace()
    async def process_payment_account(self, update: Update, model: PaymentAccountProcess):
        """

        :param update:
        :param model:
        :return:
        """
        message = update.effective_message.text
        try:
            await self._exchaige_assistant_provider.send_payment_account(
                message=message,
                customer_id=model.customer_id,
                session_id=model.session_id
            )
        except Exception as e:
            logger.exception(e)
            await update.effective_message.reply_text(
                text="Sorry, something went wrong\. Please try again later\.",
                parse_mode=ParseMode.MARKDOWN_V2
            )
            return
        await update.effective_message.reply_text(text="Thank you for your cooperation.")

    @distributed_trace()
    async def payment_account_status(self, update: Update, context: CustomContext) -> None:
        """

        :param update:
        :param context:
        :return:
        """
        message = PaymentAccountStatusMessage.format()
        buttons = InlineKeyboardMarkup(
            [
                (
                    InlineKeyboardButton(
                        text="Preparing",
                        callback_data=f"PA_STATUS {PaymentAccountStatus.PREPARING.value}"
                    ),
                    InlineKeyboardButton(
                        text="Out of stock",
                        callback_data=f"PA_STATUS {PaymentAccountStatus.OUT_OF_STOCK.value}"
                    ),
                )
            ]
        )
        await update.effective_message.reply_text(
            text=message.text,
            parse_mode=message.parse_mode,
            reply_markup=buttons
        )

    @distributed_trace()
    async def update_payment_account_status(self, update: Update, context: CustomContext) -> None:
        """

        :param update:
        :param context:
        :return:
        """
        callback_query = update.callback_query
        _, status = cast(str, callback_query.data).split()
        try:
            await self._exchaige_assistant_provider.update_payment_account_status(
                group_id=update.effective_chat.id,
                status=PaymentAccountStatus(status)
            )
            edit_text = f"{update.effective_message.text_markdown_v2}"
            await update.effective_message.edit_text(
                text=edit_text,
                parse_mode=ParseMode.MARKDOWN_V2
            )
        except Exception as e:
            logger.exception(e)
            await update.effective_message.reply_text(
                text="Sorry, something went wrong\. Please try again later\.",
                parse_mode=ParseMode.MARKDOWN_V2
            )
            return

    # --------------------------------------------------
    # [Flow] confirm pay
    @distributed_trace()
    async def confirm_pay(self, update: Update, context: CustomContext) -> None:
        """

        :param update:
        :param context:
        :return:
        """
        callback_query = update.callback_query
        _, customer_id, session_id = cast(str, callback_query.data).split()
        try:
            await self._exchaige_assistant_provider.confirm_pay(
                customer_id=int(customer_id),
                session_id=session_id
            )
            await update.effective_message.edit_reply_markup()
        except Exception as e:
            logger.exception(e)
            await update.effective_message.reply_text(
                text="Sorry, something went wrong\. Please try again later\.",
                parse_mode=ParseMode.MARKDOWN_V2
            )
            return
        await update.effective_message.reply_text(text="Thank you for your cooperation.")
