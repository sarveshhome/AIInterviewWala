"""Dependency Injection container.

Composition root: wires concrete implementations to interfaces and provides
factory functions for FastAPI's Depends(). Single place to swap implementations.
"""
from __future__ import annotations

from functools import lru_cache

from application.commands.auth_commands import (
    LoginUseCase, OAuthLoginUseCase, RefreshTokenUseCase, RegisterUseCase,
)
from application.commands.interview_commands import (
    CompleteInterviewUseCase, StartInterviewUseCase, SubmitAnswerUseCase,
)
from application.commands.resume_commands import (
    BuildLearningRoadmapUseCase, CareerCoachUseCase, UploadResumeUseCase,
)
from application.queries.queries import GetDashboardQuery, GetInterviewHistoryQuery
from application.unit_of_work import IUnitOfWork
from domain.interfaces.repositories import ICache
from domain.interfaces.services import (
    IAuthService, ICareerAI, IInterviewAI, ILLMService, IOAuthProvider, IResumeParser, ITokenIssuer,
)
from domain.value_objects.value_objects import Provider
from infrastructure.auth.jwt_service import JWTAuthService, TokenIssuer
from infrastructure.auth.oauth import build_oauth_providers
from infrastructure.cache.redis_cache import RedisCache
from infrastructure.database.unit_of_work import MongoUnitOfWork
from infrastructure.external.cohere.career_ai import CohereCareerAI
from infrastructure.external.cohere.cohere_service import CohereService
from infrastructure.external.cohere.interview_ai import CohereInterviewAI
from infrastructure.external.resume_parser import ResumeParser


class Container:
    """Lazy singleton container. Build once at app startup."""
    def __init__(self):
        self._cache: ICache | None = None
        self._auth: IAuthService | None = None
        self._issuer: ITokenIssuer | None = None
        self._llm: ILLMService | None = None
        self._interview_ai: IInterviewAI | None = None
        self._career_ai: ICareerAI | None = None
        self._parser: IResumeParser | None = None
        self._oauth: dict[Provider, IOAuthProvider] | None = None

    # --- services (singletons) ---
    def cache(self) -> ICache:
        if self._cache is None:
            self._cache = RedisCache()
        return self._cache

    def auth(self) -> IAuthService:
        if self._auth is None:
            self._auth = JWTAuthService()
        return self._auth

    def issuer(self) -> ITokenIssuer:
        if self._issuer is None:
            self._issuer = TokenIssuer(self.auth())
        return self._issuer

    def llm(self) -> ILLMService:
        if self._llm is None:
            self._llm = CohereService()
        return self._llm

    def interview_ai(self) -> IInterviewAI:
        if self._interview_ai is None:
            self._interview_ai = CohereInterviewAI(self.llm())
        return self._interview_ai

    def career_ai(self) -> ICareerAI:
        if self._career_ai is None:
            self._career_ai = CohereCareerAI(self.llm())
        return self._career_ai

    def parser(self) -> IResumeParser:
        if self._parser is None:
            self._parser = ResumeParser()
        return self._parser

    def oauth_providers(self) -> dict[Provider, IOAuthProvider]:
        if self._oauth is None:
            self._oauth = build_oauth_providers()
        return self._oauth

    def uow(self) -> IUnitOfWork:
        return MongoUnitOfWork()

    # --- use cases (factories) ---
    def register_use_case(self):
        return RegisterUseCase(self.uow(), self.auth(), self.issuer())

    def login_use_case(self):
        return LoginUseCase(self.uow(), self.auth(), self.issuer())

    def oauth_login_use_case(self):
        return OAuthLoginUseCase(self.uow(), self.oauth_providers(), self.issuer())

    def refresh_use_case(self):
        return RefreshTokenUseCase(self.uow(), self.auth(), self.issuer())

    def start_interview_use_case(self):
        return StartInterviewUseCase(self.uow(), self.interview_ai())

    def submit_answer_use_case(self):
        return SubmitAnswerUseCase(self.uow(), self.interview_ai())

    def complete_interview_use_case(self):
        return CompleteInterviewUseCase(self.uow(), self.interview_ai())

    def upload_resume_use_case(self):
        return UploadResumeUseCase(self.uow(), self.parser(), self.career_ai())

    def career_coach_use_case(self):
        return CareerCoachUseCase(self.uow(), self.career_ai())

    def roadmap_use_case(self):
        return BuildLearningRoadmapUseCase(self.uow(), self.career_ai())

    def dashboard_query(self):
        return GetDashboardQuery(self.uow())

    def history_query(self):
        return GetInterviewHistoryQuery(self.uow())


@lru_cache
def get_container() -> Container:
    return Container()