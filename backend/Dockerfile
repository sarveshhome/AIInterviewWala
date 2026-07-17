# Multi-stage build for the FastAPI backend
FROM python:3.12-slim AS builder

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1

COPY requirements.txt .
RUN pip install --user -r requirements.txt

# ---- runtime ----
FROM python:3.12-slim

WORKDIR /app
ENV PYTHONPATH=/app PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /root/.local /root/.local
COPY . .

EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
  CMD curl -fs http://localhost:8000/api/v1/health || exit 1

CMD ["uvicorn", "presentation.app:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]