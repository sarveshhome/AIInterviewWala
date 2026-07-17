"""Interview-related commands: start, answer, complete."""
from __future__ import annotations

from uuid import UUID

from application.dtos.dtos import (
    AnswerRequest,
    EvaluationResponse,
    QuestionResponse,
    StartInterviewRequest,
)
from application.unit_of_work import IUnitOfWork
from domain.entities.entities import Answer, Evaluation, Interview, Question, User
from domain.exceptions import BusinessRuleViolation, EntityNotFound
from domain.interfaces.services import IInterviewAI
from domain.value_objects.value_objects import InterviewStatus


class StartInterviewUseCase:
    def __init__(self, uow: IUnitOfWork, ai: IInterviewAI):
        self._uow = uow
        self._ai = ai

    async def execute(self, user_id: UUID, req: StartInterviewRequest) -> QuestionResponse:
        async with self._uow as uow:
            user = await uow.users.get_by_id(user_id)
            if not user:
                raise EntityNotFound("User", user_id)
            # Fetch latest resume text for personalization (optional)
            resume_text = None
            resumes = await uow.resumes.list_by_user(user_id)
            if resumes:
                resume_text = resumes[-1].content_text

            interview = Interview(
                user_id=user_id,
                type=req.type,
                technology=req.technology,
                total_questions_planned=req.total_questions,
                status=InterviewStatus.IN_PROGRESS,
            )
            await uow.interviews.add(interview)

            q_text = await self._ai.generate_first_question(
                interview_type=req.type, technology=req.technology, resume_text=resume_text
            )
            question = Question(
                interview_id=interview.id,
                type=req.type,
                topic=req.technology or req.type.value,
                text=q_text,
                order=0,
            )
            interview.current_question_order = 0
            interview.started_at = interview.created_at
            await uow.questions.add(question)
            await uow.interviews.update(interview)

        return QuestionResponse(
            id=question.id, interview_id=interview.id, type=question.type,
            topic=question.topic, difficulty=question.difficulty, text=question.text, order=question.order,
        )


class SubmitAnswerUseCase:
    """Evaluate the answer, generate the next question (one-at-a-time flow)."""
    def __init__(self, uow: IUnitOfWork, ai: IInterviewAI):
        self._uow = uow
        self._ai = ai

    async def execute(self, user_id: UUID, interview_id: UUID, req: AnswerRequest) -> EvaluationResponse:
        async with self._uow as uow:
            interview = await uow.interviews.get_by_id(interview_id)
            if not interview or interview.user_id != user_id:
                raise EntityNotFound("Interview", interview_id)
            if interview.status != InterviewStatus.IN_PROGRESS:
                raise BusinessRuleViolation("interview_not_in_progress")

            question = await uow.questions.get_by_id(req.question_id)
            if not question or question.interview_id != interview_id:
                raise EntityNotFound("Question", req.question_id)

            answer = Answer(
                question_id=question.id,
                interview_id=interview_id,
                user_id=user_id,
                text=req.text,
                code=req.code,
                language=req.language,
                duration_seconds=req.duration_seconds,
            )
            await uow.answers.add(answer)

            feedback = await self._ai.evaluate_answer(
                interview_type=interview.type, question=question.text, answer=req.text,
                technology=interview.technology, code=req.code,
            )
            evaluation = Evaluation(
                answer_id=answer.id, question_id=question.id, feedback=feedback,
            )
            await uow.evaluations.add(evaluation)

            next_question = None
            new_order = question.order + 1
            if new_order < interview.total_questions_planned:
                history = [
                    {"q": q.text, "a": a.text}
                    for q in await uow.questions.list_by_interview(interview_id)
                    for a in await uow.answers.list_by_interview(interview_id)
                    if a.question_id == q.id
                ]
                next_text = await self._ai.generate_next_question(
                    interview_type=interview.type, technology=interview.technology, history=history,
                )
                next_q = Question(
                    interview_id=interview_id, type=interview.type,
                    topic=interview.technology or interview.type.value, text=next_text, order=new_order,
                )
                await uow.questions.add(next_q)
                interview.current_question_order = new_order
                next_question = QuestionResponse(
                    id=next_q.id, interview_id=interview_id, type=next_q.type,
                    topic=next_q.topic, difficulty=next_q.difficulty, text=next_q.text, order=next_q.order,
                )
            else:
                interview.status = InterviewStatus.COMPLETED
            await uow.interviews.update(interview)

        return EvaluationResponse(answer_id=answer.id, question_id=question.id, feedback=feedback, next_question=next_question)


class CompleteInterviewUseCase:
    """Generate summary + overall score after the last question."""
    def __init__(self, uow: IUnitOfWork, ai: IInterviewAI):
        self._uow = uow
        self._ai = ai

    async def execute(self, user_id: UUID, interview_id: UUID) -> dict:
        async with self._uow as uow:
            interview = await uow.interviews.get_by_id(interview_id)
            if not interview or interview.user_id != user_id:
                raise EntityNotFound("Interview", interview_id)
            questions = await uow.questions.list_by_interview(interview_id)
            answers = await uow.answers.list_by_interview(interview_id)
            qa = [{"q": q.text, "a": next((a.text for a in answers if a.question_id == q.id), "")} for q in questions]
            result = await self._ai.summarize_interview(interview.type, qa)
            from domain.value_objects.value_objects import Score
            interview.overall_score = Score(value=result.get("overall_score", 0))
            interview.summary = result.get("summary")
            from datetime import datetime
            interview.completed_at = datetime.utcnow()
            interview.status = InterviewStatus.COMPLETED
            await uow.interviews.update(interview)
        return {"interview_id": str(interview_id), **result}