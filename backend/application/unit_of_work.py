"""Unit of Work — atomic transaction boundary across repositories.

In MongoDB (no multi-document ACID tx by default pre-5.x), the UoW coordinates
writes, dispatches domain events, and guarantees consistency semantics for the
application layer. Implemented in infrastructure with a real session/tx.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from domain.interfaces.repositories import (
    IAnalyticsRepository,
    IAnswerRepository,
    IEvaluationRepository,
    IInterviewRepository,
    ILearningRoadmapRepository,
    IQuestionRepository,
    IResumeRepository,
    IUserRepository,
)


class IUnitOfWork(ABC):
    """Exposes repositories and a commit/rollback lifecycle."""
    users: IUserRepository
    interviews: IInterviewRepository
    questions: IQuestionRepository
    answers: IAnswerRepository
    evaluations: IEvaluationRepository
    resumes: IResumeRepository
    roadmaps: ILearningRoadmapRepository
    analytics: IAnalyticsRepository

    async def __aenter__(self) -> "IUnitOfWork":
        await self.begin()
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        if exc_type is not None:
            await self.rollback()
        else:
            await self.commit()

    @abstractmethod
    async def begin(self) -> None: ...

    @abstractmethod
    async def commit(self) -> None: ...

    @abstractmethod
    async def rollback(self) -> None: ...