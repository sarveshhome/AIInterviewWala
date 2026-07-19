"""DTOs — Data Transfer Objects for crossing layer boundaries.

These decouple the presentation layer from domain entities.
"""
from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

from domain.value_objects.value_objects import Feedback, InterviewType, Provider


# ---------- Auth ----------
class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)
    full_name: str = Field(min_length=2, max_length=120)
    target_role: Optional[str] = None
    experience_years: Optional[int] = Field(default=None, ge=0, le=60)


class OAuthLoginRequest(BaseModel):
    provider: Provider
    token: str  # id_token (Google) or access token (LinkedIn)


class RefreshRequest(BaseModel):
    refresh_token: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class UserResponse(BaseModel):
    id: UUID
    email: str
    full_name: str
    is_active: bool
    is_verified: bool
    target_role: Optional[str] = None
    experience_years: Optional[int] = None


# ---------- Resume ----------
class ResumeUploadResponse(BaseModel):
    id: UUID
    user_id: UUID
    file_name: str
    ats_score: Optional[float] = None
    missing_skills: list[str] = []
    strong_areas: list[str] = []
    weak_areas: list[str] = []
    recommended_improvements: list[str] = []
    extracted_skills: list[str] = []


# ---------- Interview ----------
class StartInterviewRequest(BaseModel):
    type: InterviewType
    technology: Optional[str] = None
    total_questions: int = Field(default=10, ge=1, le=30)


class AnswerRequest(BaseModel):
    question_id: UUID
    text: str = ""
    code: Optional[str] = None
    language: Optional[str] = None
    duration_seconds: int = 0


class QuestionResponse(BaseModel):
    id: UUID
    interview_id: UUID
    type: InterviewType
    topic: str
    difficulty: str
    text: str
    order: int


class EvaluationResponse(BaseModel):
    answer_id: UUID
    question_id: UUID
    feedback: Feedback
    next_question: Optional[QuestionResponse] = None


class InterviewSummaryResponse(BaseModel):
    interview_id: UUID
    overall_score: Optional[float] = None
    summary: Optional[str] = None
    completed_at: Optional[datetime] = None


# ---------- Career ----------
class CareerCoachRequest(BaseModel):
    question: str
    goal_role: Optional[str] = None


class LearningRoadmapRequest(BaseModel):
    goal_role: str
    gaps: list[str] = []


# ---------- Analytics ----------
class ProgressPoint(BaseModel):
    """A single point on the score-over-time progress graph."""
    date: str  # ISO-8601 (completed_at / started_at / created_at)
    score: float
    label: str  # e.g. "#1 technical"


class AnalyticsResponse(BaseModel):
    total_interviews: int = 0
    average_score: Optional[float] = None
    weak_areas: list[str] = []
    strong_areas: list[str] = []
    tech_performance: dict[str, float] = {}
    history: list[dict] = []
    progress: list[ProgressPoint] = []  # score-over-time series for the progress graph


# ---------- Common ----------
class PaginationParams(BaseModel):
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)


class ErrorResponse(BaseModel):
    code: str
    message: str
    detail: Optional[dict] = None