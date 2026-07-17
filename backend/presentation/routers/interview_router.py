"""Interview router — start, answer, complete."""
from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, status

from application.dtos.dtos import AnswerRequest, EvaluationResponse, InterviewSummaryResponse, StartInterviewRequest, QuestionResponse
from presentation.dependencies.auth import get_current_user_id
from infrastructure.di.container import get_container

router = APIRouter(prefix="/interview", tags=["interview"])


@router.post("/start", response_model=QuestionResponse, status_code=status.HTTP_201_CREATED)
async def start_interview(req: StartInterviewRequest, user_id: UUID = Depends(get_current_user_id)):
    return await get_container().start_interview_use_case().execute(user_id, req)


@router.post("/answer", response_model=EvaluationResponse)
async def submit_answer(req: AnswerRequest, user_id: UUID = Depends(get_current_user_id)):
    # interview_id must be inferred from the question (kept simple here via question)
    # In production, include interview_id in the request DTO.
    container = get_container()
    async with container.uow() as uow:
        question = await uow.questions.get_by_id(req.question_id)
        interview_id = question.interview_id
    return await container.submit_answer_use_case().execute(user_id, interview_id, req)


@router.post("/{interview_id}/complete", response_model=InterviewSummaryResponse)
async def complete_interview(interview_id: UUID, user_id: UUID = Depends(get_current_user_id)):
    result = await get_container().complete_interview_use_case().execute(user_id, interview_id)
    from application.dtos.dtos import InterviewSummaryResponse as S
    return S(interview_id=interview_id, overall_score=result.get("overall_score"),
              summary=result.get("summary"), completed_at=None)