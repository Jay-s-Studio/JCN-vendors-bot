"""
Top-level package for database.
"""
from .aio_redis import RedisPool

__all__ = [
    "RedisPool",
]
