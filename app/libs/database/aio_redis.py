"""
AioRedis
"""
from redis.asyncio import Redis, from_url

from app.config import settings


class RedisPool:
    """RedisPool"""

    def __init__(self):
        uri = f"redis://:{settings.REDIS_PASSWORD}@{settings.REDIS_HOST}:{settings.REDIS_PORT}"
        if settings.REDIS_SSL:
            uri = f"rediss://{settings.REDIS_USERNAME}:{settings.REDIS_PASSWORD}@{settings.REDIS_HOST}:{settings.REDIS_PORT}"
        self._uri = uri
        self._redis = None

    def create(self) -> Redis:
        """

        :return:
        """
        if self._redis:
            return self._redis
        session = from_url(
            url=self._uri,
            password=settings.REDIS_PASSWORD,
            encoding="utf-8",
            decode_responses=True
        )
        self._redis = session
        return session
