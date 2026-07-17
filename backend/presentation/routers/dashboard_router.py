"""Dashboard + analytics router."""
from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, Query

from application.dtos.dtos import AnalyticsResponse
from presentation.dependencies.auth import get_current_user_id
from infrastructure.di.container import get_container

router = APIRouter(tags=["analytics"])


@router.get("/dashboard", response_model=AnalyticsResponse)
async def dashboard(user_id: UUID = Depends(get_current_user_id)):
    return await get_container().dashboard_query().execute(user_id)


@router.get("/analytics", response_model=AnalyticsResponse)
async def analytics(user_id: UUID = Depends(get_current_user_id)):
    return await get_container().dashboard_query().execute(user_id)


@router.get("/interviews")
async def interview_history(skip: int = Query(0, ge=0), limit: int = Query(20, ge=1, le=100),
                             user_id: UUID = Depends(get_current_user_id)):
    return await get_container().history_query().execute(user_id, skip=skip, limit=limit)