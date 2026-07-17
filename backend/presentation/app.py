"""FastAPI application factory."""
from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import _rate_limiter
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

from application.dtos.dtos import ErrorResponse
from config.settings import settings
from domain.exceptions import DomainException
from infrastructure.database.indexes import ensure_indexes
from infrastructure.database.mongodb.connection import MongoConnection
from infrastructure.observability.logging import setup_logging, setup_tracing
from presentation.middleware.middleware import RequestIDMiddleware
from presentation.routers import routers


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    await MongoConnection.connect()
    await ensure_indexes()
    setup_tracing(app)
    yield
    await MongoConnection.disconnect()


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="AI-powered interview coach. Make an impression with AI interview prep.",
        docs_url="/docs" if not settings.is_production else None,
        redoc_url="/redoc" if not settings.is_production else None,
        lifespan=lifespan,
    )

    app.state.limiter = _rate_limiter.Limiter(key_func=get_remote_address,
                                               default_limit=[settings.rate_limit_default] if settings.rate_limit_enabled else None)
    app.add_middleware(SlowAPIMiddleware)
    app.add_middleware(RequestIDMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    for router in routers:
        app.include_router(router, prefix="/api/v1")

    @app.exception_handler(DomainException)
    async def domain_exc_handler(request: Request, exc: DomainException):
        status_map = {
            "entity_not_found": 404, "duplicate_entity": 409, "invalid_credentials": 401,
            "token_expired": 401, "invalid_token": 401, "unauthorized": 401, "forbidden": 403,
            "business_rule": 422, "llm_error": 502, "rate_limited": 429,
            "resume_parse_error": 422, "unsupported_resume": 415, "unsupported_file": 415,
        }
        return JSONResponse(status_code=status_map.get(exc.code, 400),
                            content=ErrorResponse(code=exc.code, message=exc.message).model_dump())

    @app.exception_handler(RateLimitExceeded)
    async def rate_handler(request: Request, exc: RateLimitExceeded):
        return JSONResponse(status_code=429,
                            content=ErrorResponse(code="rate_limited", message=str(exc.detail)).model_dump())

    return app


app = create_app()