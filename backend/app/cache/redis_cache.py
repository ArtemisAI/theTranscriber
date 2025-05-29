"""Tiny wrapper around redis-py to simplify caching logic.

The real implementation will expose `get`, `set`, and helper methods with
JSON serialisation.  For now, we only keep placeholders so that other modules
can import the interface without breaking.
"""

from __future__ import annotations

from typing import Any, Optional

import redis.asyncio as redis_async
from app.core.config import settings


class RedisCache:
    """Singleton style cache client (async)."""

    _instance: "RedisCache | None" = None

    def __new__(cls, *args: Any, **kwargs: Any):  # noqa: D401
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.redis_url = settings.redis_url
        self.client = redis_async.from_url(
            self.redis_url, encoding="utf-8", decode_responses=True
        )
        self.default_ttl_seconds = settings.cache_ttl_seconds

    async def get(self, key: str) -> Optional[str]:  # noqa: D401
        """Retrieve a value from cache or return ``None``."""
        return await self.client.get(key)

    async def set(self, key: str, value: str, ttl: int | None = None) -> None:  # noqa: D401
        """Store a value in cache with optional TTL."""
        effective_ttl = ttl if ttl is not None else self.default_ttl_seconds
        await self.client.set(key, value, ex=effective_ttl)
