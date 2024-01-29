"""
TelegramHandler
"""
import telegram
from fastapi import HTTPException
from starlette import status
from telegram import Bot, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.constants import ParseMode

from app.libs.consts.enums import BotType
from app.libs.logger import logger
from app.providers import ExchaigeAssistantProvider
from app.serializers.v1.telegram import TelegramBroadcast


class TelegramHandler:
    """TelegramHandler"""

    def __init__(
        self,
        bot: Bot,
        exchaige_assistant_provider: ExchaigeAssistantProvider
    ):
        self._bot = bot
        self._exchaige_assistant_provider = exchaige_assistant_provider

    async def broadcast_message(self, model: TelegramBroadcast):
        """
        broadcast message
        :param model:
        :return:
        """
        # group = await self._telegram_account_provider.get_chat_group(chat_id=model.chat_id)
        # if not group:
        #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="chat group not found")
        # try:
        #     message = await self._bot.send_message(chat_id=model.chat_id, text=model.message)
        # except telegram.error.BadRequest as e:
        #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        # except Exception as e:
        #     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        # return message.to_dict()

    async def exchange_rate_msg(self):
        """
        exchange rate msg
        :return:
        """
        # chat_groups = await self._telegram_account_provider.get_chat_groups_by_bot_type(bot_type=BotType.VENDORS)
        # message = (
        #     "Please provide the latest exchange rate information, "
        #     "click \"Provide\" and reply in <strong>20 minutes</strong>."
        # )
        # buttons = InlineKeyboardMarkup([(InlineKeyboardButton("Provide", callback_data="EXCHANGE_RATE provide"),)])
        # for chat_group in chat_groups:
        #     try:
        #         await self._bot.send_message(
        #             chat_id=chat_group.id,
        #             text=message,
        #             parse_mode=ParseMode.HTML,
        #             reply_markup=buttons
        #         )
        #     except telegram.error.BadRequest as e:
        #         logger.error(e)
        #         continue
