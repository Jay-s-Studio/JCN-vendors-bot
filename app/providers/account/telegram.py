"""
AccountProvider
"""
from typing import Optional, List

from redis.asyncio import Redis

from app.clients.firebase.firestore import GoogleFirestoreClient
from app.libs.consts.enums import BotType
from app.libs.database import RedisPool
from app.libs.decorators.sentry_tracer import distributed_trace
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

    @distributed_trace()
    async def set_account(self, user_id: str, data: dict):
        """
        set account
        :param user_id:
        :param data:
        :return:
        """
        _collection = "account"
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

    @distributed_trace()
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

    @distributed_trace()
    async def update_chat_group(self, chat_id: str, data: TelegramChatGroup):
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
            raw_dict = result.to_dict()
            raw_data = TelegramChatGroup(
                id=raw_dict.get("id"),
                title=raw_dict.get("title"),
                type=raw_dict.get("type"),
                in_group=data.in_group,
                bot_type=data.bot_type,
                custom_info=raw_dict.get("custom_info")
            )
            update_data = {
                **data.model_dump(exclude={"custom_info"})
            }
            if data.custom_info.customer_service and raw_data.custom_info.customer_service is None:
                update_data["custom_info.customer_service"] = data.custom_info.customer_service.model_dump()
            await self.firestore_client.update_document(
                collection=_collection,
                document=chat_id,
                data=update_data
            )
            return
        await self.firestore_client.set_document(
            collection=_collection,
            document=chat_id,
            data=data.model_dump()
        )

    @distributed_trace()
    async def get_chat_group(self, chat_id: str) -> Optional[TelegramChatGroup]:
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
        return TelegramChatGroup(**result.to_dict())

    @distributed_trace()
    async def get_all_chat_group(self) -> List[TelegramChatGroup]:
        """
        get all chat group
        :return:
        """
        chat_groups = []
        async for item in self.firestore_client.stream(collection="chat_group"):
            chat_groups.append(TelegramChatGroup(**item.to_dict()))
        return chat_groups

    @distributed_trace()
    async def get_chat_groups_by_bot_type(self, bot_type: BotType) -> List[TelegramChatGroup]:
        """
        get chat groups by bot type
        :param bot_type:
        :return:
        """
        result: List[TelegramChatGroup] = await self.get_all_chat_group()
        chat_groups = []
        for item in result:
            if item.custom_info.bot_type == bot_type:
                chat_groups.append(item)
        return chat_groups

    @distributed_trace()
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

    @distributed_trace()
    async def get_chat_group_members(self, chat_id: str) -> List[TelegramAccount]:
        """
        get chat group members
        :param chat_id:
        :return:
        """
        _collection = f"group_member:{chat_id}"
        members = []
        async for item in self.firestore_client.stream(collection=_collection):
            members.append(TelegramAccount(**item.to_dict()))
        return members

    @distributed_trace()
    async def delete_chat_group_member(self, chat_id: str, user_id: str):
        """
        delete chat group member
        :param chat_id:
        :param user_id:
        :return:
        """
        _collection = f"group_member:{chat_id}"
        await self.firestore_client.delete_document(
            collection=_collection,
            document=user_id
        )

    @distributed_trace()
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

    @distributed_trace()
    async def delete_account_exist_group(self, user_id: str, chat_id: str):
        """
        delete account exist group
        :param user_id:
        :param chat_id:
        :return:
        """
        _collection = f"account_group:{user_id}"
        await self.firestore_client.delete_document(
            collection=_collection,
            document=chat_id
        )

    @distributed_trace()
    async def update_group_custom_info(
        self,
        chat_id: str,
        data: dict,
    ) -> bool:
        """
        update group customer service
        :param chat_id:
        :param data:
        :return:
        """
        _collection = "chat_group"
        result = await self.firestore_client.get_document(
            collection=_collection,
            document=chat_id
        )
        if not result.exists:
            return False
        await self.firestore_client.update_document(
            collection=_collection,
            document=chat_id,
            data=data
        )
        return True
