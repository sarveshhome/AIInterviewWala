"""Pytest fixtures — fakes for repositories, LLM, auth, and UoW."""
from __future__ import annotations

import asyncio
from collections import defaultdict
from datetime import datetime, timezone
from typing import Optional
from uuid import UUID, uuid4

import pytest

from application.unit_of_work import IUnitOfWork
from domain.entities.entities import (
    Analytics, Answer, Evaluation, Interview, LearningRoadmap, Question, Resume, User,
)
from domain.exceptions import InvalidCredentials
from domain.interfaces.repositories import (
    IAnalyticsRepository, IAnswerRepository, ICache, IEvaluationRepository,
    IInterviewRepository, ILearningRoadmapRepository, IQuestionRepository,
    IResumeRepository, IUserRepository,
)
from domain.interfaces.services import IAuthService, ICareerAI, IInterviewAI, ILLMService, ITokenIssuer
from domain.value_objects.value_objects import Feedback, InterviewStatus, InterviewType, Provider, Score


# ---------- In-memory repositories ----------
class InMemUserRepo(IUserRepository):
    def __init__(self): self.store = {}
    async def get_by_id(self, id): return self.store.get(str(id))
    async def list(self, filters=None, skip=0, limit=50): return list(self.store.values())
    async def add(self, e): self.store[str(e.id)] = e; return e
    async def update(self, e): self.store[str(e.id)] = e; return e
    async def delete(self, id): return self.store.pop(str(id), None) is not None
    async def get_by_email(self, email):
        return next((u for u in self.store.values() if u.email.lower() == email.lower()), None)
    async def get_by_provider_subject(self, provider, subject):
        return next((u for u in self.store.values() if u.provider.value == provider and u.provider_subject == subject), None)


class InMemRepo:
    def __init__(self, fk_field=None): self.store = {}; self.fk_field = fk_field
    async def get_by_id(self, id): return self.store.get(str(id))
    async def list(self, filters=None, skip=0, limit=50):
        items = list(self.store.values())
        if filters and self.fk_field:
            items = [i for i in items if getattr(i, self.fk_field, None) and str(getattr(i, self.fk_field)) == filters.get(self.fk_field)]
        return items
    async def add(self, e): self.store[str(e.id)] = e; return e
    async def update(self, e): self.store[str(e.id)] = e; return e
    async def delete(self, id): return self.store.pop(str(id), None) is not None


class FakeUoW(IUnitOfWork):
    def __init__(self):
        self.users = InMemUserRepo()
        self.interviews = InMemRepo()
        self.questions = InMemRepo()
        self.answers = InMemRepo()
        self.evaluations = InMemRepo()
        self.resumes = InMemRepo()
        self.roadmaps = InMemRepo()
        self.analytics = InMemRepo()
        self._committed = False
    async def begin(self): self._committed = False
    async def commit(self): self._committed = True
    async def rollback(self): pass


# ---------- Fakes for services ----------
class FakeAuth(IAuthService):
    def hash_password(self, p): return f"hashed:{p}"
    def verify_password(self, p, h): return h == f"hashed:{p}"
    def create_access_token(self, sub, extra=None): return f"access:{sub}"
    def create_refresh_token(self, sub): return f"refresh:{sub}"
    def decode_token(self, token):
        if token.startswith("refresh:"): return {"sub": token.split(":")[1], "type": "refresh"}
        if token.startswith("access:"): return {"sub": token.split(":")[1], "type": "access"}
        raise InvalidCredentials()


class FakeTokenIssuer(ITokenIssuer):
    def __init__(self, auth): self.auth = auth
    async def issue(self, user_id, email):
        from domain.value_objects.value_objects import Token
        return Token(access_token=self.auth.create_access_token(user_id),
                     refresh_token=self.auth.create_refresh_token(user_id), expires_in=1800)


class FakeLLM(ILLMService):
    async def complete(self, prompt, system=None, **kw): return "OK"
    async def complete_json(self, prompt, schema, system=None):
        return {"question": "What is your greatest weakness?"}


class FakeInterviewAI(IInterviewAI):
    async def generate_first_question(self, *a, **k): return "Tell me about a challenging project."
    async def evaluate_answer(self, *a, **k):
        return Feedback(score=Score(value=80), mistakes=["m"], ideal_answer="ideal",
                         suggested_improvements=["i"], follow_up_question="follow up?")
    async def generate_next_question(self, *a, **k): return "Next question?"
    async def summarize_interview(self, *a, **k):
        return {"overall_score": 82, "summary": "good", "strong_areas": ["s"], "weak_areas": ["w"]}


class FakeCareerAI(ICareerAI):
    async def analyze_resume(self, *a, **k):
        from domain.value_objects.value_objects import ATSReport
        return ATSReport(score=Score(value=70), missing_skills=["Kafka"], strong_areas=["Python"],
                         weak_areas=["DB"], recommended_improvements=["add metrics"])
    async def build_learning_roadmap(self, *a, **k):
        return {"title": "Roadmap", "est_total_weeks": 12, "milestones": []}
    async def career_coach(self, *a, **k):
        return {"answer": "do X", "action_items": ["a"], "resources": ["r"]}


class FakeCache(ICache):
    def __init__(self): self.store = {}
    async def get(self, k): return self.store.get(k)
    async def set(self, k, v, ttl=300): self.store[k] = v
    async def delete(self, k): self.store.pop(k, None)


@pytest.fixture
def uow(): return FakeUoW()
@pytest.fixture
def auth(): return FakeAuth()
@pytest.fixture
def issuer(auth): return FakeTokenIssuer(auth)
@pytest.fixture
def llm(): return FakeLLM()
@pytest.fixture
def interview_ai(): return FakeInterviewAI()
@pytest.fixture
def career_ai(): return FakeCareerAI()
@pytest.fixture
def cache(): return FakeCache()