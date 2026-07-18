"""MongoDB index definitions — ensure indexes at startup."""
from __future__ import annotations

import logging

from infrastructure.database.mongodb.connection import MongoConnection

logger = logging.getLogger(__name__)

INDEXES = {
    "users": [
        {"key": ("email", 1), "unique": True},
        # Dedupe OAuth subjects only. Email/password users have provider_subject
        # = null; a plain (provider, provider_subject) unique index would collide
        # for every email user. Use a partial index so only docs where
        # provider_subject exists are indexed (sparse alone is not enough — it
        # skips missing fields, not null ones).
        {"key": ("provider", 1, "provider_subject", 1), "unique": True,
         "partialFilterExpression": {"provider_subject": {"$type": "string"}}},
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
            # `key` is a flat tuple of alternating (field, direction) values,
            # e.g. ("email", 1) or ("provider", 1, "provider_subject", 1).
            # pymongo expects a list of (field, direction) pairs.
            key = spec["key"]
            pairs = list(zip(key[::2], key[1::2]))
            opts = {k: v for k, v in spec.items() if k != "key"}
            await col.create_index(pairs, **opts)
    logger.info("MongoDB indexes ensured")