"""Centralized application settings using pydantic-settings.

Single source of truth for all configuration. Injected across the app via DI.
"""
from functools import lru_cache
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="ignore"
    )

    # App
    app_name: str = "AI Interview Coach"
    app_env: str = "development"
    app_debug: bool = True
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    app_version: str = "1.0.0"
    cors_origins: str = "http://localhost:8081,http://localhost:3000"

    # MongoDB
    mongodb_uri: str = "mongodb://localhost:27017"
    mongodb_db: str = "ai_interview_coach"

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # Celery
    celery_broker_url: str = "redis://localhost:6379/1"
    celery_result_backend: str = "redis://localhost:6379/2"

    # JWT
    jwt_secret: str = Field(default="dev-secret-change-me", min_length=8)
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 14

    # Cohere
    cohere_api_key: str = ""
    cohere_model: str = "command-r-plus"
    cohere_embed_model: str = "embed-english-v3.0"

    # OAuth
    google_client_id: str = ""
    google_client_secret: str = ""
    linkedin_client_id: str = ""
    linkedin_client_secret: str = ""

    # Rate limit
    rate_limit_enabled: bool = True
    rate_limit_default: str = "60/minute"

    # Observability
    otel_exporter_otlp_endpoint: str = "http://localhost:4317"
    otel_service_name: str = "ai-interview-coach"
    log_level: str = "INFO"

    @property
    def cors_origins_list(self) -> List[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    @property
    def is_production(self) -> bool:
        return self.app_env.lower() == "production"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()