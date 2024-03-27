#!/usr/bin/env python3
"""Exercise module."""
import redis
import uuid
from typing import Union


class Cache:
    """
    A class representing a cache interface using Redis.

    This class provides methods to interact with a Redis cache,
    including storing data and retrieving it using random keys.
    """

    def __init__(self) -> None:
        """
        Initialize a new Cache instance.

        This method creates a Redis client and flushes
        the Redis database to ensure a clean cache.
        """
        self._redis: redis.Redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data in the Redis cache.

        This method generates a random key using UUID, stores
        the input data in Redis using the generated key,
        and returns the key for future retrieval.

        Args:
            data: The data to be stored in the cache.
            It can be a string, bytes, integer, or float.

        Returns:
            str: The generated key under which the data is stored in the cache.
        """
        key: str = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
