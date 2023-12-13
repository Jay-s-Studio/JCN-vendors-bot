"""
AccountProvider
"""
from typing import Optional, List

from redis.asyncio import Redis

from app.libs.consts.enums import BotType
from app.libs.database import RedisPool
from app.clients.firebase.firestore import GoogleFirestoreClient
from app.models.account.telegram import TelegramAccount, TelegramChatGroup


class TelegramAccountProvider:
    """TelegramAccountProvider"""

    def __init__(self, redis: RedisPool):
        self._redis: Redis = redis.create()
        self.firestore_client = GoogleFirestoreClient()

    @staticmethod
    def redis_name():
        """

        :return:
        """

    async def set_account(self, user_id: str, data: dict) -> Optional[TelegramAccount]:
        """
        set account
        :param user_id:
        :param data:
        :return:
        """
        try:
            await self.firestore_client.set_document(
                collection="account",
                document=user_id,
                data=data
            )
        except Exception as e:
            return None
        return TelegramAccount(**data)

    async def get_account(self, user_id: str) -> Optional[TelegramAccount]:
        """
        get account
        :param user_id:
        :return:
        """
        result = await self.firestore_client.get_document(
            collection="account",
            document=user_id
        )
        if not result.exists:
            return None
        return TelegramAccount(**result.to_dict())

    async def update_chat_group(self, chat_id: str, data: dict):
        """
        update a chat group
        :param chat_id:
        :param data:
        :return:
        """
        _collection = "chat_group"
        result = await self.firestore_client.get_document(
            collection=_collection,
            document=chat_id
        )
        if result.exists:
            await self.firestore_client.update_document(
                collection=_collection,
                document=chat_id,
                data=data
            )
            return
        await self.firestore_client.set_document(
            collection=_collection,
            document=chat_id,
            data=data
        )

    async def get_chat_group(self, chat_id: str):
        """
        get a chat group
        :param chat_id:
        :return:
        """
        result = await self.firestore_client.get_document(
            collection="chat_group",
            document=chat_id
        )
        if not result.exists:
            return None
        return result.to_dict()

    async def get_all_chat_group(self) -> List[TelegramChatGroup]:
        """
        get all chat group
        :return:
        """
        result = await self.firestore_client.stream(collection="chat_group")
        chat_groups = []
        async for item in result:
            chat_groups.append(TelegramChatGroup(**item.to_dict()))
        return chat_groups

    async def get_chat_groups_by_bot_type(self, bot_type: BotType) -> List[TelegramChatGroup]:
        """
        get chat groups by bot type
        :param bot_type:
        :return:
        """
        result = await self.get_all_chat_group()
        chat_groups = []
        for item in result:
            if item.bot_type == bot_type:
                chat_groups.append(item)
        return chat_groups

    async def update_chat_group_member(self, chat_id: str, user_id: str, data: dict):
        """
        update chat group member
        :param chat_id:
        :param user_id:
        :param data:
        :return:
        """
        _collection = f"group_member:{chat_id}"
        result = await self.firestore_client.get_document(
            collection=_collection,
            document=user_id
        )
        if result.exists:
            await self.firestore_client.update_document(
                collection=_collection,
                document=user_id,
                data=data
            )
            return
        await self.firestore_client.set_document(
            collection=_collection,
            document=user_id,
            data=data
        )

    async def update_account_exist_group(self, user_id: str, chat_id: str, data: dict):
        """
        update account exist group
        :param user_id:
        :param chat_id:
        :param data:
        :return:
        """
        _collection = f"account_group:{user_id}"
        result = await self.firestore_client.get_document(
            collection=_collection,
            document=chat_id
        )
        if result.exists:
            await self.firestore_client.update_document(
                collection=_collection,
                document=chat_id,
                data=data
            )
            return
        await self.firestore_client.set_document(
            collection=_collection,
            document=chat_id,
            data=data
        )

