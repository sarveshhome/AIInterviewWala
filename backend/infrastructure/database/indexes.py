"""MongoDB index definitions — ensure indexes at startup."""
from __future__ import annotations

import logging

from infrastructure.database.mongodb.connection import MongoConnection

logger = logging.getLogger(__name__)

INDEXES = {
    "users": [
        {"key": ("email", 1), "unique": True},
        {"key": ("provider", 1, "provider_subject", 1), "unique": True, "sparse": True},
    ],
    "interviews": [
        {"key": ("user_id", 1, "created_at", -1)},
        {"key": ("status", 1)},
    ],
    "questions": [
        {"key": ("interview_id", 1, "order", 1)},
    ],
    "answers": [
        {"key": ("interview_id", 1)},
        {"key": ("question_id", 1)},
    ],
    "evaluations": [
        {"key": ("answer_id", 1), "unique": True},
    ],
    "resumes": [
        {"key": ("user_id", 1, "created_at", -1)},
    ],
    "learningRoadmaps": [
        {"key": ("user_id", 1, "created_at", -1)},
    ],
    "analytics": [
        {"key": ("user_id", 1), "unique": True},
    ],
}


async def ensure_indexes() -> None:
    db = MongoConnection.db()
    for collection, specs in INDEXES.items():
        col = db[collection]
        for spec in specs:
            key = spec.pop("key")
            await col.create_index([key] if isinstance(key, tuple) and len(key) == 2 and not isinstance(key[0], tuple) else key, **spec)
    logger.info("MongoDB indexes ensured")