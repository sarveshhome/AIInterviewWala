"""Celery app for background tasks (resume analysis, analytics aggregation, notifications)."""
from __future__ import annotations

from celery import Celery

from config.settings import settings

celery_app = Celery(
    "ai_interview_coach",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
)
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_acks_late=True,
    worker_prefetch_multiplier=4,
    task_default_retry_delay=30,
    task_time_limit=300,
)


@celery_app.task(name="aggregate_analytics", bind=True, max_retries=3)
def aggregate_analytics(self, user_id: str) -> None:
    """Recompute a user's analytics document from interviews/evaluations (sync entrypoint)."""
    import asyncio
    from infrastructure.celery.tasks import _aggregate_analytics_async
    asyncio.run(_aggregate_analytics_async(user_id))


@celery_app.task(name="send_notification", bind=True, max_retries=3)
def send_notification(self, user_id: str, message: str) -> None:
    # Placeholder for push/email notification fan-out
    return None