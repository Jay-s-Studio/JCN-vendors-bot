"""
GoogleFirestore
"""
from typing import AsyncGenerator, AsyncIterator

from firebase_admin import firestore_async
from google.api_core import retry_async
from google.cloud.firestore_v1 import DocumentSnapshot, DocumentReference
from google.cloud.firestore_v1.types import write

from app.clients.firebase.base import firebase_app
from app.config import settings


class GoogleFirestoreClient:
    """GoogleFirestoreClient"""

    def __init__(self):
        self.db = firestore_async.client(app=firebase_app)

    @staticmethod
    def gen_collection(collection: str):
        """

        :param collection:
        :return:
        """
        if collection.startswith(f"{settings.APP_NAME}:"):
            return collection
        return f"{settings.APP_NAME}:{collection}"

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
        doc_ref = self.db.collection(collection).document(document)
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
        doc_ref = self.db.collection(collection).document(document)
        return await doc_ref.get(**kwargs)

    async def list_documents(self, collection: str, **kwargs) -> AsyncGenerator[DocumentReference, None]:
        """

        :param collection:
        :param kwargs:
        :return:
        """
        kwargs["retry"] = retry_async.AsyncRetry()
        collection = self.gen_collection(collection)
        doc_ref = self.db.collection(collection)
        return doc_ref.list_documents(**kwargs)

    async def stream(self, collection: str, **kwargs) -> AsyncIterator[DocumentSnapshot]:
        """

        :param collection:
        :param kwargs:
        :return:
        """
        kwargs["retry"] = retry_async.AsyncRetry()
        collection = self.gen_collection(collection)
        doc_ref = self.db.collection(collection)
        return doc_ref.stream(**kwargs)

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
        doc_ref = self.db.collection(collection).document(document)
        return await doc_ref.update(data, **kwargs)
