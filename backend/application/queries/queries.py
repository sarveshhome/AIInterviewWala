"""Queries (reads) — CQRS read side. Optimized, no domain mutations."""
from __future__ import annotations

from uuid import UUID

from application.dtos.dtos import AnalyticsResponse
from application.unit_of_work import IUnitOfWork
from domain.entities.entities import Analytics
from domain.exceptions import EntityNotFound


class GetDashboardQuery:
    def __init__(self, uow: IUnitOfWork):
        self._uow = uow

    async def execute(self, user_id: UUID) -> AnalyticsResponse:
        async with self._uow as uow:
            analytics = await uow.analytics.get_by_user(user_id)
            if not analytics:
                # Compute lazily from interviews/answers
                interviews = await uow.interviews.list_by_user(user_id)
                return AnalyticsResponse(
                    total_interviews=len(interviews),
                    history=[{"id": str(i.id), "type": i.type.value, "status": i.status.value,
                              "score": i.overall_score.value if i.overall_score else None} for i in interviews[:20]],
                )
            return AnalyticsResponse(
                total_interviews=analytics.total_interviews,
                average_score=analytics.average_score.value if analytics.average_score else None,
                weak_areas=analytics.weak_areas, strong_areas=analytics.strong_areas,
                tech_performance=analytics.tech_performance, history=analytics.history,
            )


class GetInterviewHistoryQuery:
    def __init__(self, uow: IUnitOfWork):
        self._uow = uow

    async def execute(self, user_id: UUID, skip: int = 0, limit: int = 50) -> list[dict]:
        async with self._uow as uow:
            interviews = await uow.interviews.list_by_user(user_id, skip=skip, limit=limit)
            return [{"id": str(i.id), "type": i.type.value, "technology": i.technology,
                     "status": i.status.value, "score": i.overall_score.value if i.overall_score else None}
                    for i in interviews]