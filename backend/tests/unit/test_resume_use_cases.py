"""Unit tests for resume/career use cases."""
import pytest
from uuid import uuid4

from application.commands.resume_commands import (
    BuildLearningRoadmapUseCase, CareerCoachUseCase, UploadResumeUseCase,
)
from application.dtos.dtos import CareerCoachRequest, LearningRoadmapRequest
from domain.entities.entities import User


@pytest.mark.asyncio
async def test_upload_resume_returns_ats(uow, career_ai):
    from domain.interfaces.services import IResumeParser

    class FakeParser(IResumeParser):
        def parse(self, content, mime_type, file_name): return "fake resume text"

    user_id = uuid4()
    await uow.users.add(User(id=user_id, email="a@b.com", full_name="A"))
    resp = await UploadResumeUseCase(uow, FakeParser(), career_ai).execute(user_id, b"x", "text/plain", "r.pdf")
    assert resp.ats_score == 70
    assert "Kafka" in resp.missing_skills


@pytest.mark.asyncio
async def test_career_coach(uow, career_ai):
    user_id = uuid4()
    await uow.users.add(User(id=user_id, email="a@b.com", full_name="A"))
    resp = await CareerCoachUseCase(uow, career_ai).execute(user_id, CareerCoachRequest(question="How to grow?"))
    assert resp["answer"] == "do X"


@pytest.mark.asyncio
async def test_build_roadmap(uow, career_ai):
    user_id = uuid4()
    await uow.users.add(User(id=user_id, email="a@b.com", full_name="A"))
    resp = await BuildLearningRoadmapUseCase(uow, career_ai).execute(
        user_id, LearningRoadmapRequest(goal_role="Staff Engineer", gaps=["System Design"]))
    assert resp["est_total_weeks"] == 12