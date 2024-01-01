"""
GoogleFirestore
"""
from typing import AsyncIterator

from firebase_admin import firestore_async
from google.api_core import retry_async
from google.cloud.firestore_v1 import DocumentSnapshot, AsyncCollectionReference
from google.cloud.firestore_v1.types import write

from app.clients.firebase.base import firebase_app
from app.config import settings


class GoogleFirestoreClient:
    """GoogleFirestoreClient"""

    def __init__(self):
        self.db = firestore_async.client(app=firebase_app)

    def gen_collection(self, collection: str) -> AsyncCollectionReference:
        """

        :param collection:
        :return:
        """
        if not collection.startswith(f"{settings.APP_NAME}:"):
            collection = f"{settings.APP_NAME}:{collection}"
        return self.db.collection(collection)

    async def set_document(self, collection: str, document: str, data: dict, **kwargs) -> write.WriteResult:
        """

        :param collection:
        :param document:
        :param data:
        :param kwargs:
        :return:
        """
        kwargs["retry"] = retry_async.AsyncRetry()
        collection = self.gen_collection(collection)
        doc_ref = collection.document(document)
        return await doc_ref.set(data, **kwargs)

    async def get_document(self, collection: str, document: str, **kwargs) -> DocumentSnapshot:
        """

        :param collection:
        :param document:
        :param kwargs:
        :return:
        """
        kwargs["retry"] = retry_async.AsyncRetry()
        collection = self.gen_collection(collection)
        doc_ref = collection.document(document)
        return await doc_ref.get(**kwargs)

    async def stream(self, collection: str, **kwargs) -> AsyncIterator[DocumentSnapshot]:
        """

        :param collection:
        :param kwargs:
        :return:
        """
        kwargs["retry"] = retry_async.AsyncRetry()
        collection: AsyncCollectionReference = self.gen_collection(collection)
        return collection.stream(**kwargs)

    async def update_document(self, collection: str, document: str, data: dict, **kwargs) -> write.WriteResult:
        """

        :param collection:
        :param document:
        :param data:
        :param kwargs:
        :return:
        """
        kwargs["retry"] = retry_async.AsyncRetry()
        collection = self.gen_collection(collection)
        doc_ref = collection.document(document)
        return await doc_ref.update(data, **kwargs)

    async def delete_document(self, collection: str, document: str, **kwargs) -> write.WriteResult:
        """

        :param collection:
        :param document:
        :param kwargs:
        :return:
        """
        kwargs["retry"] = retry_async.AsyncRetry()
        collection = self.gen_collection(collection)
        doc_ref = collection.document(document)
        return await doc_ref.delete(**kwargs)
