"""Celery worker entrypoint: `celery -A worker.celery_app worker -l info`."""
from infrastructure.celery.celery_app import celery_app  # noqa: F401