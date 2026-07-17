"""Career router — career coach + learning roadmap."""
from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends

from application.dtos.dtos import CareerCoachRequest, LearningRoadmapRequest
from presentation.dependencies.auth import get_current_user_id
from infrastructure.di.container import get_container

router = APIRouter(prefix="/career", tags=["career"])


@router.post("/coach")
async def career_coach(req: CareerCoachRequest, user_id: UUID = Depends(get_current_user_id)):
    return await get_container().career_coach_use_case().execute(user_id, req)


@router.post("/roadmap")
async def build_roadmap(req: LearningRoadmapRequest, user_id: UUID = Depends(get_current_user_id)):
    return await get_container().roadmap_use_case().execute(user_id, req)