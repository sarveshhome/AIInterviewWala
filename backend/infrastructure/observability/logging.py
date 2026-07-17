"""Structured logging (structlog) + OpenTelemetry setup."""
from __future__ import annotations

import logging
import sys

import structlog
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from opentelemetry.instrumentation.redis import RedisInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from config.settings import settings


def setup_logging() -> None:
    """Configure structlog with JSON output in prod, console in dev."""
    logging.basicConfig(format="%(message)s", stream=sys.stdout, level=settings.log_level)
    processors = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
    ]
    if settings.is_production:
        processors.append(structlog.processors.JSONRenderer())
    else:
        processors.append(structlog.dev.ConsoleRenderer())
    structlog.configure(processors=processors, wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
                        cache_logger_on_first_use=True)


def setup_tracing(app=None) -> None:
    """Configure OTel tracer provider + auto-instrumentation."""
    resource = Resource.create({"service.name": settings.otel_service_name, "environment": settings.app_env})
    provider = TracerProvider(resource=resource)
    provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter(endpoint=settings.otel_exporter_otlp_endpoint, insecure=True)))
    trace.set_tracer_provider(provider)
    RedisInstrumentor().instrument()
    HTTPXClientInstrumentor().instrument()
    if app is not None:
        FastAPIInstrumentor.instrument_app(app)


def get_logger(name: str = __name__):
    return structlog.get_logger(name)