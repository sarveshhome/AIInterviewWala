# AI Interview Coach 🎯

> **Make an impression with AI interview prep.**

A production-ready, enterprise-grade mobile-first application that helps experienced
software engineers prepare for interviews using AI (Cohere LLM). Conducts mock
technical, coding, behavioral, system-design, and voice interviews; evaluates answers
with scores, ideal answers, and follow-ups; analyzes resumes (ATS); recommends
learning roadmaps; and tracks progress through an analytics dashboard.

---

## Tech Stack

| Layer | Stack |
|---|---|
| Frontend | React Native, Redux Toolkit, TanStack Query, React Navigation, Axios, React Hook Form, MMKV, NativeWind, Reanimated, Victory Charts |
| Backend | Python, FastAPI, Clean Architecture, CQRS, Repository + UoW, DI, DDD, JWT, OpenTelemetry, Redis, Celery, Docker |
| Database | MongoDB Atlas |
| AI | Cohere LLM API |

---

## Quick Start

### Backend
```bash
cd backend
cp .env.example .env   # fill COHERE_API_KEY, MONGODB_URI, JWT_SECRET
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn presentation.app:app --reload
# API at http://localhost:8000/docs
```

### Full stack (Docker)
```bash
cp backend/.env.example backend/.env   # fill secrets
docker-compose up --build
# api :8000 | mongo :27017 | redis :6379 | otel :4317
```

### Tests
```bash
cd backend
pytest tests/unit tests/integration -v
```

### Mobile
```bash
cd mobile
yarn install
yarn android   # or: yarn ios
yarn start     # Metro bundler on :8081
```

---

## API (base `/api/v1`)

See interactive docs at `/docs` once running. Key endpoints:

```
POST /auth/register | /auth/login | /auth/oauth | /auth/refresh
POST /resume/upload
POST /interview/start | /interview/answer | /interview/{id}/complete
POST /career/coach  | /career/roadmap
GET  /dashboard | /analytics | /interviews
GET  /health | /ready
```

---

## Project Layout

```
backend/   FastAPI clean architecture (domain/application/infrastructure/presentation/config/tests)
mobile/    React Native feature architecture (features/core/shared/navigation/services)
infra/     Docker, Kubernetes manifests, MongoDB schema
docs/      ARCHITECTURE.md (all 30 PRD deliverables)
.github/   CI/CD pipeline
docker-compose.yml
```

See **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)** for the full architecture,
diagrams, domain model, use cases, sequence/class diagrams, MongoDB schema,
security, caching, monitoring, rate limiting, production checklist, coding
standards, and the step-by-step implementation plan.

---

## Features

- **Auth**: email + Google + LinkedIn + JWT (access/refresh)
- **Resume**: PDF/DOCX parsing, ATS score, skill/experience extraction
- **AI Technical Interview** (one question at a time, evaluate, score, ideal answer, next question)
- **Coding Interview** (correctness/performance/complexity/naming/architecture/security/best practices)
- **Behavioral Interview** (STAR → leadership/communication/ownership/conflict/decision-making)
- **System Design Interview** (scalability/caching/messaging/DB/load balancing/trade-offs/security/cloud)
- **Voice Interview** (STT → AI eval → TTS)
- **AI Career Coach** (learning roadmap, career growth, salary, leadership, architecture)
- **Analytics Dashboard** (history, average score, weak/strong areas, progress graph, tech-wise performance)

---

## Security & Production

JWT, bcrypt, CORS allowlist, rate limiting, secrets via env/K8s, structured logs
with correlation IDs, OpenTelemetry tracing, health/readiness probes, HPA + PDB +
TLS ingress. Full checklist in `docs/ARCHITECTURE.md`.

---


https://github.com/user-attachments/assets/e9224a3b-f1d3-4bf0-8c17-0a7b89a83dce


---

## License

MIT — example project. Replace placeholder secrets before any deployment.
