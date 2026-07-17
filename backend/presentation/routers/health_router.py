"""Health & readiness probes."""
from __future__ import annotations

from fastapi import APIRouter

from config.settings import settings

router = APIRouter(tags=["health"])


@router.get("/health")
async def health():
    return {"status": "ok", "service": settings.app_name, "version": settings.app_version}


@router.get("/ready")
async def ready():
    from infrastructure.database.mongodb.connection import MongoConnection
    try:
        await MongoConnection.db().command("ping")
        return {"status": "ready", "db": "ok"}
    except Exception as e:  # noqa: BLE001
        return {"status": "not_ready", "db": str(e)}