"""Value Objects — immutable, self-validating domain concepts.

Value objects have no identity; they are defined by their attributes.
They enforce invariants at construction time (fail fast).
"""
from __future__ import annotations

from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4

from pydantic import BaseModel, EmailStr, Field, field_validator


class UserId(BaseModel):
    value: UUID = Field(default_factory=uuid4)


class SkillLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class InterviewType(str, Enum):
    TECHNICAL = "technical"
    CODING = "coding"
    BEHAVIORAL = "behavioral"
    SYSTEM_DESIGN = "system_design"
    VOICE = "voice"


class InterviewStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ABORTED = "aborted"


class Provider(str, Enum):
    EMAIL = "email"
    GOOGLE = "google"
    LINKEDIN = "linkedin"


class Email(EmailStr):
    """Strongly-typed email (validated by pydantic EmailStr)."""


class Score(BaseModel):
    """A bounded score 0-100. Enforces range invariant."""
    value: float = Field(ge=0, le=100)

    @field_validator("value")
    @classmethod
    def round_to_half(cls, v: float) -> float:
        return round(v, 1)


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class ATSReport(BaseModel):
    score: Score
    missing_skills: list[str] = []
    strong_areas: list[str] = []
    weak_areas: list[str] = []
    recommended_improvements: list[str] = []


class Feedback(BaseModel):
    score: Score
    mistakes: list[str] = []
    ideal_answer: str | None = None
    suggested_improvements: list[str] = []
    follow_up_question: str | None = None


class Timestamps(BaseModel):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class Paginated(BaseModel):
    """Generic pagination envelope value object."""
    items: list
    total: int
    page: int
    page_size: int