"""Repository interfaces (ports) — contracts the infrastructure layer must implement.

Following the Dependency Inversion Principle: domain defines the interface,
infrastructure provides the MongoDB implementation.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, Optional, TypeVar
from uuid import UUID

from domain.entities.entities import (
    Analytics,
    Answer,
    Evaluation,
    Interview,
    LearningRoadmap,
    Question,
    Resume,
    User,
)

T = TypeVar("T")


class IGenericRepository(ABC, Generic[T]):
    @abstractmethod
    async def get_by_id(self, id: UUID) -> Optional[T]:
        ...

    @abstractmethod
    async def list(self, filters: Optional[dict] = None, skip: int = 0, limit: int = 50) -> list[T]:
        ...

    @abstractmethod
    async def add(self, entity: T) -> T:
        ...

    @abstractmethod
    async def update(self, entity: T) -> T:
        ...

    @abstractmethod
    async def delete(self, id: UUID) -> bool:
        ...


class IUserRepository(IGenericRepository[User]):
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        ...

    @abstractmethod
    async def get_by_provider_subject(self, provider: str, subject: str) -> Optional[User]:
        ...


class IInterviewRepository(IGenericRepository[Interview]):
    @abstractmethod
    async def list_by_user(self, user_id: UUID, skip: int = 0, limit: int = 50) -> list[Interview]:
        ...


class IQuestionRepository(IGenericRepository[Question]):
    @abstractmethod
    async def list_by_interview(self, interview_id: UUID) -> list[Question]:
        ...

    @abstractmethod
    async def get_by_order(self, interview_id: UUID, order: int) -> Optional[Question]:
        ...


class IAnswerRepository(IGenericRepository[Answer]):
    @abstractmethod
    async def list_by_interview(self, interview_id: UUID) -> list[Answer]:
        ...


class IEvaluationRepository(IGenericRepository[Evaluation]):
    @abstractmethod
    async def get_by_answer(self, answer_id: UUID) -> Optional[Evaluation]:
        ...


class IResumeRepository(IGenericRepository[Resume]):
    @abstractmethod
    async def list_by_user(self, user_id: UUID) -> list[Resume]:
        ...


class ILearningRoadmapRepository(IGenericRepository[LearningRoadmap]):
    @abstractmethod
    async def get_latest_by_user(self, user_id: UUID) -> Optional[LearningRoadmap]:
        ...


class IAnalyticsRepository(IGenericRepository[Analytics]):
    @abstractmethod
    async def get_by_user(self, user_id: UUID) -> Optional[Analytics]:
        ...


class ICache(ABC):
    @abstractmethod
    async def get(self, key: str) -> Optional[str]:
        ...

    @abstractmethod
    async def set(self, key: str, value: str, ttl: int = 300) -> None:
        ...

    @abstractmethod
    async def delete(self, key: str) -> None:
        ...