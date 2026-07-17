"""Middleware — request logging, correlation IDs, error handling."""
from __future__ import annotations

import time
import uuid

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from infrastructure.observability.logging import get_logger

logger = get_logger("middleware")


class RequestIDMiddleware(BaseHTTPMiddleware):
    """Attach a correlation ID to every request and response."""
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        request.state.request_id = request_id
        start = time.perf_counter()
        response = await call_next(request)
        elapsed = (time.perf_counter() - start) * 1000
        response.headers["X-Request-ID"] = request_id
        logger.info("request", method=request.method, path=request.url.path,
                    status=response.status_code, ms=round(elapsed, 1), request_id=request_id)
        return response