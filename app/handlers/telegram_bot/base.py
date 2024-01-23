"""
TelegramBotMessagesHandler
"""
import abc
import asyncio
from typing import Optional, Tuple

from telegram import Update, ChatMemberUpdated, ChatMember, Chat

from app.config import settings
from app.context import CustomContext
from app.libs.database import RedisPool
from app.libs.decorators.sentry_tracer import distributed_trace
from app.libs.logger import logger
from app.models.account.telegram import CustomGroupInfo, TelegramAccount, TelegramChatGroup, CustomAccountInfo
from app.providers import TelegramAccountProvider


class TelegramBotBaseHandler:
    """TelegramBotMessagesHandler"""

    def __init__(
        self,
        redis: RedisPool,
        telegram_account_provider: TelegramAccountProvider
    ):
        self._redis = redis.create()
        self._telegram_account_provider = telegram_account_provider

    @abc.abstractmethod
    async def receive_message(self, update: Update, context: CustomContext) -> None:
        """
        receive message
        :param update:
        :param context:
        :return:
        """
        raise NotImplementedError()

    @staticmethod
    def extract_status_change(chat_member_update: ChatMemberUpdated) -> Optional[Tuple[bool, bool]]:
        """
        Takes a ChatMemberUpdated instance and extracts whether the 'old_chat_member' was a member
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

    @distributed_trace()
    async def setup_account_info(
        self,
        telegram_account: TelegramAccount,
        telegram_chat_group: TelegramChatGroup,
        user_custom_info: CustomAccountInfo = None,
        chat_custom_info: CustomGroupInfo = None
    ) -> None:
        """
        setup account info
        :param telegram_account:
        :param telegram_chat_group:
        :param user_custom_info:
        :param chat_custom_info:
        :return:
        """
        user_id = str(telegram_account.id)
        chat_id = str(telegram_chat_group.id)
        if user_custom_info is None:
            user_custom_info = CustomAccountInfo()
        if chat_custom_info is None:
            chat_custom_info = CustomGroupInfo()
        telegram_account.custom_info = user_custom_info
        telegram_chat_group.custom_info = chat_custom_info
        user_data = telegram_account.model_dump()
        group_chat_data = telegram_chat_group.model_dump(exclude_none=True)
        tasks = [
            self._telegram_account_provider.set_account(user_id=user_id, data=user_data),
            self._telegram_account_provider.update_chat_group(chat_id=chat_id, data=telegram_chat_group),
            self._telegram_account_provider.update_chat_group_member(chat_id=chat_id, user_id=user_id, data=user_data),
            self._telegram_account_provider.update_account_exist_group(user_id=user_id, chat_id=chat_id, data=group_chat_data)
        ]
        await asyncio.gather(*tasks)

    @distributed_trace()
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
                logger.info(f"Leaving chat {chat.title} ({chat.id})")
                await chat.send_message(text="Sorry, This bot only work in groups. I'll leave now. Bye!")
                await asyncio.sleep(2)
                await chat.leave()
                return
            except Exception as exc:
                logger.exception(exc)

        await self.setup_account_info(
            telegram_account=TelegramAccount(**update.effective_user.to_dict()),
            telegram_chat_group=TelegramChatGroup(
                **chat.to_dict(),
                in_group=is_member,
                bot_type=settings.TELEGRAM_BOT_TYPE
            ),
            chat_custom_info=CustomGroupInfo(
                customer_service=TelegramAccount(
                    **update.effective_user.to_dict(),
                    custom_info=CustomAccountInfo()
                )
            )
        )

    @distributed_trace()
    async def new_member_handler(self, update: Update, context: CustomContext) -> None:
        """

        :param update:
        :param context:
        :return:
        """
        for new_member in update.message.new_chat_members:
            if new_member.is_bot:
                continue
            await self.setup_account_info(
                telegram_account=TelegramAccount(**new_member.to_dict()),
                telegram_chat_group=TelegramChatGroup(
                    **update.effective_chat.to_dict(),
                    in_group=True,
                    bot_type=settings.TELEGRAM_BOT_TYPE
                ),
            )

    @distributed_trace()
    async def left_member_handler(self, update: Update, context: CustomContext) -> None:
        """

        :param update:
        :param context:
        :return:
        """
        for left_member in update.message.left_chat_member:
            if left_member.is_bot:
                continue
            await self._telegram_account_provider.delete_chat_group_member(
                chat_id=str(update.effective_chat.id),
                user_id=str(left_member.id)
            )
            await self._telegram_account_provider.delete_account_exist_group(
                user_id=str(left_member.id),
                chat_id=str(update.effective_chat.id)
            )
