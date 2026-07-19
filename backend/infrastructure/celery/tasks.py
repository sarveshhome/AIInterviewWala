"""Async helpers used by Celery tasks. Keep sync wrappers in celery_app.py."""
from __future__ import annotations

import logging
from datetime import datetime
from uuid import UUID

from infrastructure.database.mongodb.connection import MongoConnection
from infrastructure.database.repositories.repositories import (
    AnalyticsRepository, EvaluationRepository, InterviewRepository,
)
from domain.entities.entities import Analytics
from domain.value_objects.value_objects import InterviewStatus, Score

logger = logging.getLogger(__name__)


async def _aggregate_analytics_async(user_id: str) -> None:
    await MongoConnection.connect()
    interviews = await InterviewRepository().list_by_user(UUID(user_id))
    completed = [i for i in interviews if i.status == InterviewStatus.COMPLETED and i.overall_score]
    if not completed:
        return
    # Chronological order for the progress graph + history.
    completed.sort(key=lambda i: (i.completed_at or i.started_at or i.created_at))
    avg = sum(i.overall_score.value for i in completed) / len(completed)
    tech_perf: dict[str, list[float]] = {}
    for i in completed:
        if i.technology:
            tech_perf.setdefault(i.technology, []).append(i.overall_score.value)
    progress: list[dict] = []
    history: list[dict] = []
    for n, i in enumerate(completed, start=1):
        ts = i.completed_at or i.started_at or i.created_at
        history.append({"id": str(i.id), "type": i.type.value, "technology": i.technology,
                        "score": i.overall_score.value,
                        "completed_at": ts.isoformat() if ts else None})
        progress.append({"date": ts.isoformat() if ts else "",
                         "score": float(i.overall_score.value),
                         "label": f"#{n} {i.type.value}"})
    analytics = Analytics(
        user_id=UUID(user_id),
        total_interviews=len(completed),
        average_score=Score(value=round(avg, 1)),
        tech_performance={k: round(sum(v) / len(v), 1) for k, v in tech_perf.items()},
        history=history[-20:],
        progress=progress,
    )
    analytics.updated_at = datetime.utcnow()
    col = AnalyticsRepository()._col()
    await col.update_one({"user_id": str(user_id)}, {"$set": analytics.model_dump(mode="json")}, upsert=True)
    logger.info("Aggregated analytics for user %s", user_id)