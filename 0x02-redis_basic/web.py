#!/usr/bin/env python3
"""A module for caching data using Redis."""

import requests
import redis
import functools


def count_calls(func):
    """Decorator to count the number of times a function is called."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        url = args[0]
        redis_client = redis.Redis()
        redis_client.incr(f"count:{url}")
        return func(*args, **kwargs)
    return wrapper


def cache_result(expiration_time):
    """Decorator to cache the result of a function with an expiration time."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            url = args[0]
            redis_client = redis.Redis()
            key = f"cache:{url}"
            cached_result = redis_client.get(key)
            if cached_result:
                return cached_result.decode('utf-8')
            result = func(*args, **kwargs)
            redis_client.setex(key, expiration_time, result)
            return result
        return wrapper
    return decorator


@count_calls
@cache_result(expiration_time=10)
def get_page(url: str) -> str:
    """
    Retrieve the HTML content of a URL and return it.

    Args:
        url (str): The URL of the page to retrieve.

    Returns:
        str: The HTML content of the page.
    """
    response = requests.get(url)
    return response.text


# Example usage:
if __name__ == "__main__":
    # Simulate a slow response
    url = "http://slowwly.robertomurray.co.uk"
    print(get_page(url))

    # Example of accessing the same URL again (should be cached)
    print(get_page(url))
