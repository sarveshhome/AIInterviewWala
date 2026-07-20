"""Integration tests for the FastAPI app with a fake DI container override."""
import pytest
from fastapi.testclient import TestClient

from presentation.app import create_app
from infrastructure.di.container import get_container


@pytest.fixture
def client(monkeypatch):
    # Override container to use fake services (avoid Mongo/Cohere in CI)
    import presentation.dependencies.auth as auth_dep
    from tests.conftest import FakeUoW, FakeAuth, FakeTokenIssuer, FakeLLM, FakeInterviewAI, FakeCareerAI, FakeCache
    from infrastructure.external.resume_parser import ResumeParser

    class FakeContainer:
        def __init__(self):
            self._auth = FakeAuth()
            self._uow = FakeUoW()
        def auth(self): return self._auth
        def issuer(self): return FakeTokenIssuer(self._auth)
        def uow(self): return self._uow
        def interview_ai(self): return FakeInterviewAI()
        def career_ai(self): return FakeCareerAI()
        def parser(self): return ResumeParser()
        def oauth_providers(self): return {}
        def register_use_case(self):
            from application.commands.auth_commands import RegisterUseCase
            return RegisterUseCase(self.uow(), self.auth(), self.issuer())
        def login_use_case(self):
            from application.commands.auth_commands import LoginUseCase
            return LoginUseCase(self.uow(), self.auth(), self.issuer())
        def oauth_login_use_case(self):
            from application.commands.auth_commands import OAuthLoginUseCase
            return OAuthLoginUseCase(self.uow(), self.oauth_providers(), self.issuer())
        def refresh_use_case(self):
            from application.commands.auth_commands import RefreshTokenUseCase
            return RefreshTokenUseCase(self.uow(), self.auth(), self.issuer())
        def start_interview_use_case(self):
            from application.commands.interview_commands import StartInterviewUseCase
            return StartInterviewUseCase(self.uow(), self.interview_ai())
        def submit_answer_use_case(self):
            from application.commands.interview_commands import SubmitAnswerUseCase
            return SubmitAnswerUseCase(self.uow(), self.interview_ai())
        def complete_interview_use_case(self):
            from application.commands.interview_commands import CompleteInterviewUseCase
            return CompleteInterviewUseCase(self.uow(), self.interview_ai())
        def upload_resume_use_case(self):
            from application.commands.resume_commands import UploadResumeUseCase
            return UploadResumeUseCase(self.uow(), self.parser(), self.career_ai())
        def career_coach_use_case(self):
            from application.commands.resume_commands import CareerCoachUseCase
            return CareerCoachUseCase(self.uow(), self.career_ai())
        def roadmap_use_case(self):
            from application.commands.resume_commands import BuildLearningRoadmapUseCase
            return BuildLearningRoadmapUseCase(self.uow(), self.career_ai())
        def dashboard_query(self):
            from application.queries.queries import GetDashboardQuery
            return GetDashboardQuery(self.uow())
        def history_query(self):
            from application.queries.queries import GetInterviewHistoryQuery
            return GetInterviewHistoryQuery(self.uow())

    import importlib
    import infrastructure.di.container as cont_mod
    # presentation/routers/__init__.py re-binds submodule names to the router
    # objects, so `import presentation.routers.auth_router as ...` yields the
    # APIRouter, not the module. Resolve the real module objects instead.
    auth_r = importlib.import_module("presentation.routers.auth_router")
    career_r = importlib.import_module("presentation.routers.career_router")
    dash_r = importlib.import_module("presentation.routers.dashboard_router")
    int_r = importlib.import_module("presentation.routers.interview_router")
    resume_r = importlib.import_module("presentation.routers.resume_router")
    # Routers import get_container by value, so patch the symbol in every
    # module that holds a reference — patching only the container module
    # leaves the routers bound to the real (Mongo-backed) container. A single
    # shared instance keeps the UoW store alive across requests in one test
    # (e.g. register then login).
    fake_container = FakeContainer()
    for mod in (cont_mod, auth_dep, auth_r, career_r, dash_r, int_r, resume_r):
        monkeypatch.setattr(mod, "get_container", lambda: fake_container)

    # The app lifespan connects to Mongo and ensures indexes; stub those out so
    # the test runs without a live MongoDB (CI has none). The faked container
    # above already keeps request handling off Mongo. Also stub setup_tracing
    # (called in create_app) so the OTLP exporter doesn't spend ~60s retrying
    # localhost:4317 on process exit.
    import presentation.app as app_mod
    import infrastructure.database.mongodb.connection as mongo_mod

    async def _noop(*a, **k):
        return None

    def _noop_sync(*a, **k):
        return None

    monkeypatch.setattr(app_mod, "ensure_indexes", _noop)
    monkeypatch.setattr(app_mod, "setup_tracing", _noop_sync)
    monkeypatch.setattr(mongo_mod.MongoConnection, "connect", _noop)
    monkeypatch.setattr(mongo_mod.MongoConnection, "disconnect", _noop)

    app = create_app()
    with TestClient(app, raise_server_exceptions=False) as c:
        yield c


def test_register_endpoint(client):
    resp = client.post("/api/v1/auth/register",
                        json={"email": "x@y.com", "password": "secret123", "full_name": "X Y"})
    assert resp.status_code == 201
    assert "access_token" in resp.json()


def test_login_endpoint(client):
    client.post("/api/v1/auth/register", json={"email": "x@y.com", "password": "secret123", "full_name": "X Y"})
    resp = client.post("/api/v1/auth/login", json={"email": "x@y.com", "password": "secret123"})
    assert resp.status_code == 200
    assert "access_token" in resp.json()