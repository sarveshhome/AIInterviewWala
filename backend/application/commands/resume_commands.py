"""Resume upload + career coach commands."""
from __future__ import annotations

from uuid import UUID

from application.dtos.dtos import CareerCoachRequest, LearningRoadmapRequest, ResumeUploadResponse
from application.unit_of_work import IUnitOfWork
from domain.entities.entities import Resume
from domain.exceptions import EntityNotFound
from domain.interfaces.services import ICareerAI, IResumeParser


class UploadResumeUseCase:
    def __init__(self, uow: IUnitOfWork, parser: IResumeParser, career_ai: ICareerAI):
        self._uow = uow
        self._parser = parser
        self._career_ai = career_ai

    async def execute(self, user_id: UUID, content: bytes, mime_type: str, file_name: str) -> ResumeUploadResponse:
        text = self._parser.parse(content, mime_type, file_name)
        async with self._uow as uow:
            user = await uow.users.get_by_id(user_id)
            if not user:
                raise EntityNotFound("User", user_id)
            ats = await self._career_ai.analyze_resume(text, user.target_role)
            resume = Resume(
                user_id=user_id,
                file_name=file_name,
                content_text=text,
                mime_type=mime_type,
                ats_report=ats,
                extracted_skills=ats.strong_areas + ats.missing_skills,
                extracted_experience=[],
            )
            await uow.resumes.add(resume)
        return ResumeUploadResponse(
            id=resume.id, user_id=user_id, file_name=file_name,
            ats_score=ats.score.value, missing_skills=ats.missing_skills,
            strong_areas=ats.strong_areas, weak_areas=ats.weak_areas,
            recommended_improvements=ats.recommended_improvements,
            extracted_skills=resume.extracted_skills,
        )


class CareerCoachUseCase:
    def __init__(self, uow: IUnitOfWork, career_ai: ICareerAI):
        self._uow = uow
        self._career_ai = career_ai

    async def execute(self, user_id: UUID, req: CareerCoachRequest) -> dict:
        async with self._uow as uow:
            user = await uow.users.get_by_id(user_id)
            if not user:
                raise EntityNotFound("User", user_id)
            profile = {
                "full_name": user.full_name, "target_role": user.target_role,
                "experience_years": user.experience_years,
            }
        return await self._career_ai.career_coach(profile, req.question)


class BuildLearningRoadmapUseCase:
    def __init__(self, uow: IUnitOfWork, career_ai: ICareerAI):
        self._uow = uow
        self._career_ai = career_ai

    async def execute(self, user_id: UUID, req: LearningRoadmapRequest) -> dict:
        async with self._uow as uow:
            user = await uow.users.get_by_id(user_id)
            if not user:
                raise EntityNotFound("User", user_id)
            profile = {"full_name": user.full_name, "experience_years": user.experience_years}
        return await self._career_ai.build_learning_roadmap(profile, req.gaps, req.goal_role)