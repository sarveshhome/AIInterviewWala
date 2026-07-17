"""Redis cache — implements ICache with JSON string values & TTL."""
from __future__ import annotations

import logging
from typing import Optional

import redis.asyncio as redis

from config.settings import settings
from domain.interfaces.repositories import ICache

logger = logging.getLogger(__name__)


class RedisCache(ICache):
    def __init__(self):
        self._client = redis.from_url(settings.redis_url, decode_responses=True)

    async def get(self, key: str) -> Optional[str]:
        try:
            return await self._client.get(key)
        except Exception:  # noqa: BLE001  fail-open on cache errors
            logger.warning("Redis get failed for %s", key)
            return None

    async def set(self, key: str, value: str, ttl: int = 300) -> None:
        try:
            await self._client.set(key, value, ex=ttl)
        except Exception:  # noqa: BLE001
            logger.warning("Redis set failed for %s", key)

    async def delete(self, key: str) -> None:
        try:
            await self._client.delete(key)
        except Exception:  # noqa: BLE001
            logger.warning("Redis delete failed for %s", key)