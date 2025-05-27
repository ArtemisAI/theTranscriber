"""Tiny wrapper around redis-py to simplify caching logic.

The real implementation will expose `get`, `set`, and helper methods with
JSON serialisation.  For now, we only keep placeholders so that other modules
can import the interface without breaking.
"""

from __future__ import annotations

from typing import Any, Optional

# TODO: Uncomment once `redis` package is added to requirements
# import redis.asyncio as redis_async


class RedisCache:
    """Singleton style cache client (async)."""

    _instance: "RedisCache | None" = None

    def __new__(cls, *args: Any, **kwargs: Any):  # noqa: D401
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, url: str):
        # Placeholder: the actual connection would be initialised here
        self.url = url
        self.client = None  # type: ignore

    async def get(self, key: str) -> Optional[str]:  # noqa: D401
        """Retrieve a value from cache or return ``None``."""
        # Placeholder implementation
        return None

    async def set(self, key: str, value: str, ttl: int | None = None) -> None:  # noqa: D401
        """Store a value in cache with optional TTL."""
        # Placeholder implementation
        return None
