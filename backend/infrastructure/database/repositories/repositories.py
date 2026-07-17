"""MongoDB repository implementations (adapters) for domain interfaces.

Each repository maps between BSON documents and domain entities.
"""
from __future__ import annotations

from typing import Optional
from uuid import UUID

from infrastructure.database.mongodb.connection import MongoConnection
from infrastructure.database.serialization import to_doc, to_entity
from domain.entities.entities import (
    Analytics, Answer, Evaluation, Interview, LearningRoadmap, Question, Resume, User,
)
from domain.exceptions import EntityNotFound
from domain.interfaces.repositories import (
    IAnalyticsRepository, IAnswerRepository, IEvaluationRepository, IGenericRepository,
    IInterviewRepository, ILearningRoadmapRepository, IQuestionRepository,
    IResumeRepository, IUserRepository,
)


class MongoRepository(IGenericRepository):
    """Generic Mongo repository; subclasses set the collection name + entity type."""
    collection_name: str = ""
    entity_cls = None

    def _col(self):
        return MongoConnection.db()[self.collection_name]

    async def get_by_id(self, id: UUID) -> Optional[object]:
        doc = await self._col().find_one({"_id": str(id)})
        return to_entity(doc, self.entity_cls) if doc else None

    async def list(self, filters: Optional[dict] = None, skip: int = 0, limit: int = 50) -> list:
        cursor = self._col().find(filters or {}).skip(skip).limit(limit)
        docs = await cursor.to_list(length=limit)
        return [to_entity(d, self.entity_cls) for d in docs]

    async def add(self, entity) -> object:
        await self._col().insert_one(to_doc(entity))
        return entity

    async def update(self, entity) -> object:
        await self._col().replace_one({"_id": str(entity.id)}, to_doc(entity), upsert=True)
        return entity

    async def delete(self, id: UUID) -> bool:
        res = await self._col().delete_one({"_id": str(id)})
        return res.deleted_count > 0


class UserRepository(MongoRepository, IUserRepository):
    collection_name = "users"
    entity_cls = User

    async def get_by_email(self, email: str) -> Optional[User]:
        doc = await self._col().find_one({"email": email.lower()})
        return to_entity(doc, User) if doc else None

    async def get_by_provider_subject(self, provider: str, subject: str) -> Optional[User]:
        doc = await self._col().find_one({"provider": provider, "provider_subject": subject})
        return to_entity(doc, User) if doc else None


class InterviewRepository(MongoRepository, IInterviewRepository):
    collection_name = "interviews"
    entity_cls = Interview

    async def list_by_user(self, user_id: UUID, skip: int = 0, limit: int = 50) -> list[Interview]:
        return await self.list({"user_id": str(user_id)}, skip=skip, limit=limit)


class QuestionRepository(MongoRepository, IQuestionRepository):
    collection_name = "questions"
    entity_cls = Question

    async def list_by_interview(self, interview_id: UUID) -> list[Question]:
        return await self.list({"interview_id": str(interview_id)}, limit=100)

    async def get_by_order(self, interview_id: UUID, order: int) -> Optional[Question]:
        doc = await self._col().find_one({"interview_id": str(interview_id), "order": order})
        return to_entity(doc, Question) if doc else None


class AnswerRepository(MongoRepository, IAnswerRepository):
    collection_name = "answers"
    entity_cls = Answer

    async def list_by_interview(self, interview_id: UUID) -> list[Answer]:
        return await self.list({"interview_id": str(interview_id)}, limit=100)


class EvaluationRepository(MongoRepository, IEvaluationRepository):
    collection_name = "evaluations"
    entity_cls = Evaluation

    async def get_by_answer(self, answer_id: UUID) -> Optional[Evaluation]:
        doc = await self._col().find_one({"answer_id": str(answer_id)})
        return to_entity(doc, Evaluation) if doc else None


class ResumeRepository(MongoRepository, IResumeRepository):
    collection_name = "resumes"
    entity_cls = Resume

    async def list_by_user(self, user_id: UUID) -> list[Resume]:
        return await self.list({"user_id": str(user_id)}, limit=20)


class LearningRoadmapRepository(MongoRepository, ILearningRoadmapRepository):
    collection_name = "learningRoadmaps"
    entity_cls = LearningRoadmap

    async def get_latest_by_user(self, user_id: UUID) -> Optional[LearningRoadmap]:
        docs = await self._col().find({"user_id": str(user_id)}).sort("created_at", -1).limit(1).to_list(1)
        return to_entity(docs[0], LearningRoadmap) if docs else None


class AnalyticsRepository(MongoRepository, IAnalyticsRepository):
    collection_name = "analytics"
    entity_cls = Analytics

    async def get_by_user(self, user_id: UUID) -> Optional[Analytics]:
        doc = await self._col().find_one({"user_id": str(user_id)})
        return to_entity(doc, Analytics) if doc else None