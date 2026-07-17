"""Service interfaces (ports) for external integrations: AI, auth, file parsing."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Optional

from domain.value_objects.value_objects import (
    ATSReport,
    Feedback,
    InterviewType,
    Provider,
    Token,
)


class ILLMService(ABC):
    """Abstract LLM provider so we can swap Cohere / OpenAI without touching use cases."""

    @abstractmethod
    async def complete(self, prompt: str, system: Optional[str] = None, **kwargs) -> str:
        ...

    @abstractmethod
    async def complete_json(self, prompt: str, schema: dict, system: Optional[str] = None) -> dict:
        ...


class ICohereService(ILLMService):
    """Marker — Cohere-specific LLM implementation."""


class IAuthService(ABC):
    @abstractmethod
    def create_access_token(self, subject: str, extra: Optional[dict] = None) -> str:
        ...

    @abstractmethod
    def create_refresh_token(self, subject: str) -> str:
        ...

    @abstractmethod
    def decode_token(self, token: str) -> dict:
        ...

    @abstractmethod
    def verify_password(self, plain: str, hashed: str) -> bool:
        ...

    @abstractmethod
    def hash_password(self, plain: str) -> str:
        ...


class IOAuthProvider(ABC):
    @abstractmethod
    async def verify(self, token: str) -> dict:
        """Verify a provider token/id_token and return normalized profile dict."""
        ...


class IResumeParser(ABC):
    @abstractmethod
    def parse(self, content: bytes, mime_type: str, file_name: str) -> str:
        """Extract raw text from a resume file."""
        ...


class IInterviewAI(ABC):
    """High-level interview orchestration AI capabilities."""

    @abstractmethod
    async def generate_first_question(self, interview_type: InterviewType, technology: Optional[str],
                                       resume_text: Optional[str] = None) -> str:
        ...

    @abstractmethod
    async def evaluate_answer(self, interview_type: InterviewType, question: str, answer: str,
                               technology: Optional[str] = None, code: Optional[str] = None) -> Feedback:
        ...

    @abstractmethod
    async def generate_next_question(self, interview_type: InterviewType, technology: Optional[str],
                                      history: list[dict]) -> str:
        ...

    @abstractmethod
    async def summarize_interview(self, interview_type: InterviewType, qa_pairs: list[dict]) -> dict:
        ...


class ICareerAI(ABC):
    @abstractmethod
    async def analyze_resume(self, resume_text: str, target_role: Optional[str] = None) -> ATSReport:
        ...

    @abstractmethod
    async def build_learning_roadmap(self, profile: dict, gaps: list[str], goal_role: str) -> dict:
        ...

    @abstractmethod
    async def career_coach(self, profile: dict, question: str) -> dict:
        ...


class ITokenIssuer(ABC):
    @abstractmethod
    async def issue(self, user_id: str, email: str) -> Token:
        ...