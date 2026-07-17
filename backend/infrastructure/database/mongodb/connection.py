"""MongoDB connection management using Motor (async driver)."""
from __future__ import annotations

from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from config.settings import settings


class MongoConnection:
    """Singleton-ish MongoDB client holder. Lifecycle managed by the app."""
    _client: Optional[AsyncIOMotorClient] = None
    _db: Optional[AsyncIOMotorDatabase] = None

    @classmethod
    async def connect(cls) -> AsyncIOMotorDatabase:
        if cls._db is None:
            cls._client = AsyncIOMotorClient(
                settings.mongodb_uri,
                maxPoolSize=50,
                minPoolSize=5,
                serverSelectionTimeoutMS=5000,
                uuidRepresentation="standard",
            )
            cls._db = cls._client[settings.mongodb_db]
        return cls._db

    @classmethod
    async def disconnect(cls) -> None:
        if cls._client:
            cls._client.close()
            cls._client = None
            cls._db = None

    @classmethod
    def db(cls) -> AsyncIOMotorDatabase:
        if cls._db is None:
            raise RuntimeError("MongoDB not initialized. Call MongoConnection.connect() first.")
        return cls._db