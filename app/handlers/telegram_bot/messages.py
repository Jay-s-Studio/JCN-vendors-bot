"""
TelegramBotMessagesHandler
"""
import asyncio
from typing import Optional, Tuple

from telegram import Update, ForceReply, ChatMemberUpdated, ChatMember, Chat
from telegram.constants import ParseMode

from app.config import settings
from app.context import CustomContext
from app.libs.database import RedisPool
from app.libs.logger import logger
from app.providers import TelegramAccountProvider


class TelegramBotMessagesHandler:
    """TelegramBotMessagesHandler"""

    def __init__(
        self,
        redis: RedisPool,
        telegram_account_provider: TelegramAccountProvider
    ):
        self._redis = redis.create()
        self._telegram_account_provider = telegram_account_provider

    @staticmethod
    def extract_status_change(chat_member_update: ChatMemberUpdated) -> Optional[Tuple[bool, bool]]:
        """Takes a ChatMemberUpdated instance and extracts whether the 'old_chat_member' was a member
        of the chat and whether the 'new_chat_member' is a member of the chat. Returns None, if
        the status didn't change.
        """
        status_change = chat_member_update.difference().get("status")
        old_is_member, new_is_member = chat_member_update.difference().get("is_member", (None, None))
        logger.info(f"status_change: {status_change}")
        logger.info(f"old_is_member: {old_is_member}")
        logger.info(f"new_is_member: {new_is_member}")

        if status_change is None:
            return None

        old_status, new_status = status_change
        was_member = old_status in [
            ChatMember.MEMBER,
            ChatMember.OWNER,
            ChatMember.ADMINISTRATOR,
        ] or (old_status == ChatMember.RESTRICTED and old_is_member is True)
        is_member = new_status in [
            ChatMember.MEMBER,
            ChatMember.OWNER,
            ChatMember.ADMINISTRATOR,
        ] or (new_status == ChatMember.RESTRICTED and new_is_member is True)

        return was_member, is_member

    async def receive_message(self, update: Update, context: CustomContext) -> None:
        """
        receive message
        :param update:
        :param context:
        :return:
        """
        user = update.effective_user.to_dict()
        chat_group = update.effective_chat.to_dict()
        tasks = [
            self._telegram_account_provider.set_account(user_id=str(update.effective_user.id), data=user),
            self._telegram_account_provider.update_chat_group_member(
                chat_id=str(chat_group["id"]),
                user_id=str(update.effective_user.id),
                data=user
            ),
            self._telegram_account_provider.update_account_exist_group(
                user_id=str(update.effective_user.id),
                chat_id=str(chat_group["id"]),
                data=chat_group
            )
        ]
        await asyncio.gather(*tasks)
        if str(update.effective_user.id) == "6534924832":
            await update.effective_message.reply_text("You are shit!")
            return
        await update.effective_message.reply_text(update.message.text)

    async def track_chats(self, update: Update, context: CustomContext) -> None:
        """

        :param update:
        :param context:
        :return:
        """
        result = self.extract_status_change(update.my_chat_member)
        if result is None:
            return

        was_member, is_member = result

        # Handle chat types differently:
        chat = update.effective_chat
        if chat.type not in [Chat.GROUP, Chat.SUPERGROUP]:
            try:
                await chat.send_message(
                    f"Sorry, This bot only work in groups. I'll leave now. Bye!"
                )
                await asyncio.sleep(2)
                await chat.leave()
            except Exception as exc:
                logger.exception(exc)

        data = chat.to_dict()
        data["in_group"] = is_member
        data["bot_type"] = settings.TELEGRAM_BOT_TYPE.value
        await self._telegram_account_provider.update_chat_group(chat_id=str(chat.id), data=data)

    async def new_member_handler(self, update: Update, context: CustomContext) -> None:
        """

        :param update:
        :param context:
        :return:
        """
        for new_member in update.message.new_chat_members:
            if new_member.is_bot:
                continue
            chat_group = update.effective_chat.to_dict()
            user = new_member.to_dict()
            tasks = [
                self._telegram_account_provider.set_account(user_id=str(new_member.id), data=user),
                self._telegram_account_provider.update_chat_group_member(
                    chat_id=str(update.effective_chat.id),
                    user_id=str(new_member.id),
                    data=user
                ),
                self._telegram_account_provider.update_account_exist_group(
                    user_id=str(new_member.id),
                    chat_id=str(update.effective_chat.id),
                    data=chat_group
                )
            ]
            await asyncio.gather(*tasks)

    async def provide_exchange_rate(self, update: Update, context: CustomContext) -> None:
        """
        provide exchange rate
        :param update:
        :param context:
        :return:
        """
        await update.effective_chat.send_message(
            text="Please follow this format to provide the exchange rate for USDT: "
                 "<code>{currency}:{buy_rate}|{sell_rate}</code>.\n"
                 "Example: <code>USD:1.00|0.98,CNY:6.50|6.30,JPY:110.00|108.00</code>",
            parse_mode=ParseMode.HTML,
            reply_markup=ForceReply(selective=False)
        )
