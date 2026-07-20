"""Unit tests for interview use cases."""
import pytest
from uuid import uuid4

from application.commands.interview_commands import (
    CompleteInterviewUseCase, StartInterviewUseCase, SubmitAnswerUseCase,
)
from application.dtos.dtos import AnswerRequest, StartInterviewRequest
from domain.entities.entities import User
from domain.value_objects.value_objects import InterviewType


async def _seed_user(uow, user_id):
    await uow.users.add(User(id=user_id, email="a@b.com", full_name="A"))


@pytest.mark.asyncio
async def test_start_interview_returns_first_question(uow, interview_ai):
    user_id = uuid4()
    await _seed_user(uow, user_id)
    uc = StartInterviewUseCase(uow, interview_ai)
    q = await uc.execute(user_id, StartInterviewRequest(type=InterviewType.TECHNICAL, technology="Python"))
    assert q.text == "Tell me about a challenging project."
    assert q.order == 0


@pytest.mark.asyncio
async def test_submit_answer_evaluates_and_advances(uow, interview_ai):
    user_id = uuid4()
    await _seed_user(uow, user_id)
    start = StartInterviewUseCase(uow, interview_ai)
    q = await start.execute(user_id, StartInterviewRequest(type=InterviewType.TECHNICAL, technology="Python",
                                                           total_questions=3))
    ev = await SubmitAnswerUseCase(uow, interview_ai).execute(
        user_id, q.interview_id, AnswerRequest(question_id=q.id, text="my answer"))
    assert ev.feedback.score.value == 80
    assert ev.next_question is not None
    assert ev.next_question.order == 1


@pytest.mark.asyncio
async def test_complete_interview_summarizes(uow, interview_ai):
    user_id = uuid4()
    await _seed_user(uow, user_id)
    q = await StartInterviewUseCase(uow, interview_ai).execute(
        user_id, StartInterviewRequest(type=InterviewType.TECHNICAL, technology="Python", total_questions=1))
    await SubmitAnswerUseCase(uow, interview_ai).execute(
        user_id, q.interview_id, AnswerRequest(question_id=q.id, text="answer"))
    result = await CompleteInterviewUseCase(uow, interview_ai).execute(user_id, q.interview_id)
    assert result["overall_score"] == 82