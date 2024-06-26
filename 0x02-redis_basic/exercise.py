#!/usr/bin/env python3
"""A module for caching data using Redis."""
import redis
import uuid
from functools import wraps
from typing import Union, Callable, Optional


def count_calls(method: Callable) -> Callable:
    """
    Decorator to count the number of times a method is called.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The decorated method.
    """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function to count the number of times a method is called.

        Args:
            self: The instance of the class.
            *args: Positional arguments passed to the method.
            **kwargs: Keyword arguments passed to the method.

        Returns:
            Any: The result of the method call.
        """
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of
    inputs and outputs for a function in Redis.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The decorated method.
    """
    key_inputs = f"{method.__qualname__}:inputs"
    key_outputs = f"{method.__qualname__}:outputs"

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function to store the history of
        inputs and outputs for a function in Redis.

        Args:
            self: The instance of the class.
            *args: Positional arguments passed to the method.
            **kwargs: Keyword arguments passed to the method.

        Returns:
            Any: The result of the method call.
        """
        # Store input arguments
        self._redis.rpush(key_inputs, str(args))

        # Execute the wrapped function to get the output
        result = method(self, *args, **kwargs)

        # Store the output
        self._redis.rpush(key_outputs, str(result))

        return result

    return wrapper


class Cache:
    """A simple caching class using Redis."""

    def __init__(self):
        """
        Initialize a new Cache instance.

        This creates an instance of the Redis client
        and flushes the Redis database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data in the cache and return a unique key.

        Args:
            data (Union[str, bytes, int, float]):
            The data to be stored in the cache.

        Returns:
            str: A unique key associated with the stored data.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[
                str, bytes, int, float]:
        """
        Retrieve data from the cache using the provided key.

        Args:
            key (str): The key associated with the stored data.
            fn (Callable, optional): A callable function to convert
            the data back to the desired format.

        Returns:
            Union[str, bytes, int, float, None]: The retrieved
            data or None if the key does not exist.
        """
        data = self._redis.get(key)
        if data is not None and fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> Union[str, None]:
        """
        Retrieve data from the cache and convert it to a string.

        Args:
            key (str): The key associated with the stored data.

        Returns:
            Union[str, None]: The retrieved data as a
            string or None if the key does not exist.
        """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Union[int, None]:
        """
        Retrieve data from the cache and convert it to an integer.

        Args:
            key (str): The key associated with the stored data.

        Returns:
            Union[int, None]: The retrieved data as an integer or
            None if the key does not exist.
        """
        return self.get(key, fn=int)

    def replay(self, method: Callable):
        """
        Display the history of calls for a particular function.

        Args:
            method (Callable): The function for which to display the history.
        """
        key_inputs = f"{method.__qualname__}:inputs"
        key_outputs = f"{method.__qualname__}:outputs"

        inputs = self._redis.lrange(key_inputs, 0, -1)
        outputs = self._redis.lrange(key_outputs, 0, -1)

        print(f"{method.__qualname__} was called {len(inputs)} times:")
        for input_args, output_key in zip(inputs, outputs):
            output_data = self._redis.get(output_key)
            input_str = f"{method.__qualname__}{input_args.decode()}"
            output_str = output_data.decode()
            print(f"{input_str} -> {output_str}")
