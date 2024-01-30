"""
TelegramBotMessagesHandler
"""
import abc
import asyncio
from typing import Optional, Tuple

from telegram import Update, ChatMemberUpdated, ChatMember, Chat, User

from app.config import settings
from app.context import CustomContext
from app.libs.database import RedisPool
from app.libs.decorators.sentry_tracer import distributed_trace
from app.libs.logger import logger
from app.providers import ExchaigeAssistantProvider
from app.schemas.account.telegram import TelegramAccount, TelegramChatGroup


class TelegramBotBaseHandler:
    """TelegramBotMessagesHandler"""

    def __init__(
        self,
        redis: RedisPool,
        exchaige_assistant_provider: ExchaigeAssistantProvider
    ):
        self._redis = redis.create()
        self._exchaige_assistant_provider = exchaige_assistant_provider

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
        account: TelegramAccount,
        chat_group: TelegramChatGroup,
        is_customer_service: bool = False
    ) -> None:
        """
        setup account info
        :param account:
        :param chat_group:
        :param is_customer_service:
        :return:
        """
        tasks = [
            self._exchaige_assistant_provider.set_account(account=account),
            self._exchaige_assistant_provider.set_group(group=chat_group)
        ]
        await asyncio.gather(*tasks)
        data = {
            "account_id": account.id,
            "chat_group_id": chat_group.id,
            "is_customer_service": is_customer_service
        }
        await self._exchaige_assistant_provider.init_chat_group_member(data=data)

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
            account=TelegramAccount(**update.effective_user.to_dict()),
            chat_group=TelegramChatGroup(
                **chat.to_dict(),
                in_group=is_member,
                bot_type=settings.TELEGRAM_BOT_TYPE
            ),
            is_customer_service=True
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
                account=TelegramAccount(**new_member.to_dict()),
                chat_group=TelegramChatGroup(
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
        left_member: User = update.message.left_chat_member
        if left_member.is_bot:
            return
        await self._exchaige_assistant_provider.delete_chat_group_member(
            account_id=left_member.id,
            group_id=update.effective_chat.id
        )
