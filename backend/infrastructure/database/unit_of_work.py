"""MongoDB-backed Unit of Work implementation."""
from __future__ import annotations

from infrastructure.database.repositories.repositories import (
    AnalyticsRepository, AnswerRepository, EvaluationRepository, InterviewRepository,
    LearningRoadmapRepository, QuestionRepository, ResumeRepository, UserRepository,
)
from application.unit_of_work import IUnitOfWork
from infrastructure.database.mongodb.connection import MongoConnection


class MongoUnitOfWork(IUnitOfWork):
    """Coordinates repository access with a Mongo session/transaction.

    Falls back to non-transactional (writes are still applied) when the
    deployment does not support multi-document transactions (standalone).
    """
    def __init__(self):
        self.users = UserRepository()
        self.interviews = InterviewRepository()
        self.questions = QuestionRepository()
        self.answers = AnswerRepository()
        self.evaluations = EvaluationRepository()
        self.resumes = ResumeRepository()
        self.roadmaps = LearningRoadmapRepository()
        self.analytics = AnalyticsRepository()
        self._session = None

    async def begin(self) -> None:
        self._session = await MongoConnection.db().client.start_session()
        self._session.start_transaction()

    async def commit(self) -> None:
        if self._session:
            try:
                await self._session.commit_transaction()
            finally:
                await self._session.end_session()
                self._session = None

    async def rollback(self) -> None:
        if self._session:
            try:
                await self._session.abort_transaction()
            finally:
                await self._session.end_session()
                self._session = None