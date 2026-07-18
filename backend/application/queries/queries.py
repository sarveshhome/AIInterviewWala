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
            if analytics:
                return AnalyticsResponse(
                    total_interviews=analytics.total_interviews,
                    average_score=analytics.average_score.value if analytics.average_score else None,
                    weak_areas=analytics.weak_areas, strong_areas=analytics.strong_areas,
                    tech_performance=analytics.tech_performance, history=analytics.history,
                )
            # No precomputed analytics doc (the Celery aggregator isn't running in
            # dev) — aggregate live from interviews + answers + evaluations so the
            # dashboard actually shows data.
            return await self._aggregate(uow, user_id)

    async def _aggregate(self, uow: IUnitOfWork, user_id: UUID) -> AnalyticsResponse:
        interviews = await uow.interviews.list_by_user(user_id)
        tech_scores: dict[str, list[float]] = {}
        all_scores: list[float] = []
        history: list[dict] = []
        for iv in interviews[:50]:
            answers = await uow.answers.list_by_interview(iv.id)
            iv_scores: list[float] = []
            for a in answers:
                ev = await uow.evaluations.get_by_answer(a.id)
                if ev and ev.feedback and ev.feedback.score:
                    s = float(ev.feedback.score.value)
                    iv_scores.append(s)
                    all_scores.append(s)
                    key = iv.technology or iv.type.value
                    tech_scores.setdefault(key, []).append(s)
            overall = (iv.overall_score.value if iv.overall_score
                       else (round(sum(iv_scores) / len(iv_scores), 2) if iv_scores else None))
            history.append({"id": str(iv.id), "type": iv.type.value, "technology": iv.technology,
                            "status": iv.status.value, "score": overall})
        average_score = round(sum(all_scores) / len(all_scores), 2) if all_scores else None
        tech_performance = {k: round(sum(v) / len(v), 2) for k, v in tech_scores.items()}
        strong_areas = [k for k, v in tech_performance.items() if v >= 70]
        weak_areas = [k for k, v in tech_performance.items() if v < 50]
        return AnalyticsResponse(
            total_interviews=len(interviews),
            average_score=average_score,
            weak_areas=weak_areas,
            strong_areas=strong_areas,
            tech_performance=tech_performance,
            history=history[:20],
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