"""
TelegramBotMessagesHandler
"""
from telegram import Update, ForceReply
from telegram.constants import ParseMode

from app.config import settings
from app.context import CustomContext
from app.libs.database import RedisPool
from app.libs.decorators.sentry_tracer import distributed_trace
from app.libs.logger import logger
from app.providers import ExchaigeAssistantProvider
from app.schemas.account.telegram import TelegramAccount, TelegramChatGroup
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

        # [Flow] exchange rate process
        redis_name = self.redis_name(name=f"exchange_rate_process:{update.effective_chat.id}")
        exchange_rate_process_message_id = await self._redis.get(redis_name)
        if exchange_rate_process_message_id and str(update.message.reply_to_message.message_id) == exchange_rate_process_message_id:
            await self.parse_exchange_rate(update)
            return

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
            value=str(message.message_id),
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
