from typing import Callable, TypeVar

from django.core.cache import cache


T = TypeVar("T")


def cached(key_parts: list, compute_fn: Callable[[], T], timeout=None) -> T:
    cache_key = ":".join(str(p) for p in key_parts)

    result = cache.get(cache_key)
    if result is None:
        result = compute_fn()
        cache.set(cache_key, result, timeout=timeout)

    return result
