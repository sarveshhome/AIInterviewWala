"""Domain Entities — the core business objects of the AI Interview Coach bounded context.

Entities have identity (id) and lifecycle. They are persistence-agnostic.
"""
from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from domain.value_objects.value_objects import (
    ATSReport,
    Feedback,
    InterviewStatus,
    InterviewType,
    Provider,
    Score,
)


def _new_id() -> UUID:
    return uuid4()


class BaseEntity(BaseModel):
    """Base for all entities — provides identity and audit timestamps."""
    id: UUID = Field(default_factory=_new_id)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    def touch(self) -> None:
        self.updated_at = datetime.utcnow()


class User(BaseEntity):
    """Aggregate root for identity & auth."""
    email: str
    full_name: str
    hashed_password: Optional[str] = None
    provider: Provider = Provider.EMAIL
    provider_subject: Optional[str] = None  # OAuth sub
    is_active: bool = True
    is_verified: bool = False
    roles: list[str] = Field(default_factory=lambda: ["user"])
    target_role: Optional[str] = None  # e.g. "Senior Backend Engineer"
    experience_years: Optional[int] = None


class Question(BaseEntity):
    """A single interview question (either AI-generated or seeded)."""
    interview_id: UUID
    type: InterviewType
    topic: str
    difficulty: str = "medium"  # easy | medium | hard
    text: str
    ideal_answer: Optional[str] = None
    order: int = 0


class Answer(BaseEntity):
    """A candidate's answer to a Question."""
    question_id: UUID
    interview_id: UUID
    user_id: UUID
    text: str
    code: Optional[str] = None
    language: Optional[str] = None
    duration_seconds: int = 0


class Evaluation(BaseEntity):
    """AI evaluation of an Answer."""
    answer_id: UUID
    question_id: UUID
    feedback: Feedback
    criteria_scores: dict[str, Score] = Field(default_factory=dict)


class Interview(BaseEntity):
    """Aggregate root for an interview session."""
    user_id: UUID
    type: InterviewType
    technology: Optional[str] = None  # e.g. "Python", "Kafka", null for behavioral
    status: InterviewStatus = InterviewStatus.PENDING
    current_question_order: int = 0
    total_questions_planned: int = 10
    overall_score: Optional[Score] = None
    summary: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


class Resume(BaseEntity):
    """Aggregate root for a candidate's resume."""
    user_id: UUID
    file_name: str
    content_text: str
    mime_type: str
    ats_report: Optional[ATSReport] = None
    extracted_skills: list[str] = Field(default_factory=list)
    extracted_experience: list[str] = Field(default_factory=list)


class LearningRoadmap(BaseEntity):
    """AI-recommended learning path."""
    user_id: UUID
    title: str
    goal_role: str
    milestones: list[dict] = Field(default_factory=list)  # [{title, topics, resources, est_weeks}]
    est_total_weeks: int = 0


class Analytics(BaseEntity):
    """Per-user aggregated analytics."""
    user_id: UUID
    total_interviews: int = 0
    average_score: Optional[Score] = None
    weak_areas: list[str] = Field(default_factory=list)
    strong_areas: list[str] = Field(default_factory=list)
    tech_performance: dict[str, float] = Field(default_factory=dict)  # {tech: avg_score}
    history: list[dict] = Field(default_factory=list)  # last N interview summaries
    progress: list[dict] = Field(default_factory=list)  # [{date, score, label}] score-over-time