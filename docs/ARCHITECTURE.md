# AI Interview Coach — Architecture & Design Document

> Make an impression with AI interview prep.

This document covers the full set of deliverables required by the PRD:
architecture, diagrams, folder structure, DB design, API design, domain model,
use cases, sequence/class diagrams, MongoDB schema, deployment, security,
performance, caching, logging, monitoring, rate limiting, production-readiness
checklist, coding standards, and a step-by-step implementation plan.

---

## 1. Software Architecture

**Backend — Clean Architecture / DDD (4 concentric layers)**

```
presentation  ──►  application  ──►  domain
     ▲               │
     └── infrastructure ──┘   (implements domain interfaces)
```

- **domain/** — entities, value objects, interfaces (ports), exceptions. Pure Python, no IO.
- **application/** — use cases (commands/queries = CQRS), DTOs, Unit of Work. Depends only on domain.
- **infrastructure/** — MongoDB (motor), Redis, Cohere, JWT, OAuth, Celery, OTel, DI container. Implements domain interfaces.
- **presentation/** — FastAPI routers, middleware, dependencies, error handling.

Dependency rule: dependencies point **inward** only. Infrastructure can depend on
application/domain; neither application nor domain depends on infrastructure.

**Frontend — Feature-Based Architecture**: each vertical feature owns its
screens, components, API, hooks, Redux slice, and models. Shared `core/` holds
cross-cutting infra (store, api client, navigation, theme, storage).

---

## 2. High-Level Architecture Diagram

```
                 ┌─────────────────────────────┐
                 │      React Native App        │
                 │  (Redux Toolkit + RQ + MMKV) │
                 └──────────────┬───────────────┘
                                │ HTTPS / JWT
                 ┌──────────────▼───────────────┐
                 │       FastAPI API (x N)      │
                 │  Clean Arch + CQRS + UoW      │
                 └─────┬──────────────┬────────┘
        Cohere LLM ◄────┘              │
        (chat/embed)                   │
                ┌───────────────────────▼────────┐
                │   Redis (cache + Celery broker)│
                └──────────────────────────────┘
                                │
                 ┌──────────────▼───────────────┐
                 │   MongoDB Atlas (replica set) │
                 └──────────────────────────────┘
                                │
                 Celery worker ──► aggregates analytics, notifications
                 OpenTelemetry ──► OTel Collector ──► Jaeger/Prometheus/Grafana
```

---

## 3. Folder Structure

```
AIInterviewWala/
├── backend/                      # FastAPI clean architecture
│   ├── domain/                    # entities, value_objects, interfaces, exceptions
│   ├── application/              # use_cases (commands/queries), dtos, unit_of_work
│   ├── infrastructure/           # db (mongo), external (cohere), cache, auth, celery, di, observability
│   ├── presentation/            # routers, middleware, dependencies, app.py
│   ├── config/                  # settings
│   ├── tests/                   # unit + integration
│   ├── prompts (infrastructure/prompts)
│   ├── Dockerfile / Dockerfile.worker / main.py / worker.py / requirements.txt
├── mobile/                       # React Native feature architecture
│   └── src/{features,core,shared,navigation,services,hooks,models}
├── infra/{docker,kubernetes,ci}
├── docs/
└── docker-compose.yml
```

---

## 4. Database Design

MongoDB collections (see `infra/mongo-schema.json` for full documents):

| Collection | Purpose | Key indexes |
|---|---|---|
| users | identity & auth | unique email, (provider, provider_subject) |
| interviews | interview sessions | (user_id, created_at), status |
| questions | one question per interview step | (interview_id, order) |
| answers | candidate answers | interview_id, question_id |
| evaluations | AI feedback per answer | unique answer_id |
| feedback | (embedded in evaluations) | — |
| analytics | per-user aggregates | unique user_id |
| resume | uploaded resumes + ATS | (user_id, created_at) |
| learningRoadmap | AI roadmaps | (user_id, created_at) |

---

## 5. API Design (REST, `/api/v1`)

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | /auth/register | – | Email register |
| POST | /auth/login | – | Email login |
| POST | /auth/oauth | – | Google/LinkedIn login |
| POST | /auth/refresh | – | Refresh access token |
| POST | /resume/upload | ✔ | Upload resume → ATS analysis |
| POST | /interview/start | ✔ | Start interview → first question |
| POST | /interview/answer | ✔ | Submit answer → eval + next question |
| POST | /interview/{id}/complete | ✔ | Summarize interview |
| POST | /career/coach | ✔ | Career advice |
| POST | /career/roadmap | ✔ | Learning roadmap |
| GET  | /dashboard | ✔ | Aggregated dashboard |
| GET  | /analytics | ✔ | Analytics |
| GET  | /interviews | ✔ | Interview history |
| GET  | /health, /ready | – | Liveness/readiness |

All AI responses return structured JSON (Cohere `complete_json`).

---

## 6. Domain Model

Aggregates (entities): `User` (root), `Interview` (root), `Resume` (root),
`LearningRoadmap` (root), `Analytics` (root). `Question`, `Answer`,
`Evaluation` are entities within the Interview aggregate boundary.

Value objects: `Email`, `Score` (0–100 invariant), `ATSReport`, `Feedback`,
`Token`, `Timestamps`, enums (`InterviewType`, `InterviewStatus`, `Provider`,
`SkillLevel`).

---

## 7. Use Cases (CQRS)

**Commands** (`application/commands/`): Register, Login, OAuthLogin,
RefreshToken, StartInterview, SubmitAnswer, CompleteInterview, UploadResume,
CareerCoach, BuildLearningRoadmap.

**Queries** (`application/queries/`): GetDashboard, GetInterviewHistory.

Each use case receives `IUnitOfWork` + service interfaces via DI — fully unit-testable with fakes.

---

## 8. Sequence Diagrams

### Login
```
Client → POST /auth/login
  Router → LoginUseCase.execute(dto)
    UoW.begin → users.get_by_email → auth.verify_password
    UoW.commit
  TokenIssuer.issue → JWTAuthService.create_access/refresh_token
  ← TokenResponse
```

### Start Interview
```
Client → POST /interview/start
  StartInterviewUseCase
    UoW → resumes.list_by_user (personalize)
    InterviewRepo.add → CohereInterviewAI.generate_first_question
    QuestionRepo.add → InterviewRepo.update
  ← QuestionResponse(first question)
```

### Submit Answer
```
Client → POST /interview/answer
  SubmitAnswerUseCase
    AnswerRepo.add → CohereInterviewAI.evaluate_answer → EvaluationRepo.add
    if more questions: generate_next_question → QuestionRepo.add
    else: Interview.status = COMPLETED
  ← EvaluationResponse(feedback + next_question)
```

---

## 9. Class Diagram (simplified)

```
interface IUserRepository ──◄ UserRepository(Mongo)
interface IInterviewAI    ──◄ CohereInterviewAI(ILLMService=CohereService)
interface ICareerAI       ──◄ CohereCareerAI(ILLMService)
interface IAuthService    ──◄ JWTAuthService
interface ITokenIssuer    ──◄ TokenIssuer
interface IUnitOfWork      ──◄ MongoUnitOfWork
interface IResumeParser    ──◄ ResumeParser
interface ILLMService      ──◄ CohereService

UseCase ──uses──► IUnitOfWork, IInterviewAI/ICareerAI/IAuthService
Container ──wires──► all concrete impls (composition root)
```

---

## 10. MongoDB Schema

See `infra/mongo-schema.json`. UUIDs stored as strings (`_id`), enums as their
string values, value objects nested via pydantic dump. Indexes enforced at startup
via `ensure_indexes()`.

---

## 15-18. Docker / Compose / K8s / CI-CD

- `backend/Dockerfile`, `backend/Dockerfile.worker` (multi-stage, non-root-capable).
- `docker-compose.yml` — api, worker, mongo, redis, otel-collector, optional mobile.
- `infra/kubernetes/` — namespace, secrets, configmap, api/worker deployments,
  HPA, ingress (rate-limited + TLS), PDB.
- `.github/workflows/ci.yml` — backend tests, mobile typecheck/test, docker build, deploy.

---

## 22. Security Best Practices

- JWT access (30m) + refresh (14d); rotate refresh on use.
- Passwords hashed with bcrypt (passlib); never log secrets.
- CORS allowlist from settings; no `*` in prod.
- Secrets via env / K8s secrets, never committed (`.env.example` only).
- OAuth tokens verified server-side (Google tokeninfo / LinkedIn userinfo).
- Input validation via pydantic; file-type allowlist for uploads.
- Rate limiting (slowapi) per IP + per-user; LLM calls wrapped with backoff.
- Principle of least privilege in service accounts; TLS everywhere (ingress).

---

## 23. Performance Optimization

- Async I/O throughout (motor, httpx async, redis.asyncio) — non-blocking.
- Connection pooling (mongo maxPoolSize=50, redis pool).
- Read-side CQRS queries bypass heavy aggregate hydration where possible.
- Lazy hydration of analytics from interviews when no analytics doc exists.
- Horizontal scale via 3+ API replicas + HPA on CPU.
- Pagination defaults enforced (max 100/page).

---

## 24. Caching Strategy

- Redis cache (`RedisCache`) for: dashboard analytics, ATS reports, LLM responses
  keyed by hash(prompt+args), OAuth profile lookups.
- TTLs: analytics 5 min, ATS 1h, LLM eval 24h (deterministic prompts).
- Fail-open: cache errors logged but never break the request path.
- Invalidation: invalidate `analytics:{user_id}` on interview completion
  (Celery aggregation task rewrites the doc).

---

## 25. Logging

- `structlog` with JSON renderer in prod, console renderer in dev.
- Correlation ID per request (`X-Request-ID`) propagated to logs + OTel.
- Request log includes method/path/status/latency.
- No PII or secrets in logs; log levels from settings.

---

## 26. Monitoring

- OpenTelemetry traces (FastAPI, httpx, redis auto-instrumented) → OTel Collector.
- OTLP exporter to Jaeger/tempo; metrics to Prometheus; logs to Loki (collector-config).
- `/health` (liveness) + `/ready` (Mongo ping) probes for K8s.
- Dashboards: p95 latency, error rate, LLM call duration, Celery queue depth.

---

## 27. Rate Limiting

- slowapi global default `60/minute` (configurable), per-IP via `get_remote_address`.
- Per-endpoint overrides possible (e.g. tighter on `/auth/*`, looser on `/interview/*`).
- LLM calls additionally bounded by Celery concurrency + per-user quota (extensible).

---

## 28. Production Readiness Checklist

- [x] Health/readiness probes
- [x] Structured logs + correlation IDs
- [x] Distributed tracing (OTel)
- [x] Rate limiting + CORS allowlist
- [x] Secrets via env / K8s secrets
- [x] Multi-stage Docker images, healthcheck
- [x] HPA + PDB + multi-replica
- [x] TLS ingress (cert-manager)
- [ ] MongoDB Atlas connection encryption + IP allowlist
- [ ] Backups (Atlas snapshots) + PITR
- [ ] Cohere key rotation procedure
- [ ] Load test baseline (k6/Locust)
- [ ] Runbook for incidents

---

## 29. Coding Standards

- SOLID, DDD, Clean Architecture layering; dependencies inward only.
- CQRS: commands mutate, queries read; one use case per file/class.
- Value objects enforce invariants at construction; entities carry identity.
- DTOs at boundaries; never leak entities to/from the API directly.
- `snake_case` Python; `camelCase` JS/TS; 4-space Py, 2-space TS.
- Type hints everywhere; pydantic v2 models for validation.
- Every public interface lives in `domain/interfaces`; infrastructure provides adapters.
- Tests: unit (fakes, no IO) + integration (TestClient with DI overrides).

---

## 30. Step-by-Step Implementation Plan

1. Scaffold `backend/` clean-architecture folders + `config/settings.py`.
2. Define domain entities, value objects, interfaces, exceptions.
3. Write DTOs + Unit of Work interface.
4. Implement Mongo repositories + serialization + indexes.
5. Implement JWT auth + OAuth providers + token issuer.
6. Implement Cohere service + prompts + Interview/Career AI adapters.
7. Write use cases (commands + queries).
8. Wire DI container; build FastAPI app, routers, middleware, error handlers.
9. Add Celery worker + analytics aggregation task.
10. Add OTel + structlog; configure probes.
11. Write unit + integration tests with fakes.
12. Scaffold `mobile/` feature architecture; add core (api/store/nav/theme/storage).
13. Build auth + resume + interview features; wire RQ + Redux slices.
14. Add Docker/compose/K8s/CI; finalize docs + production checklist.