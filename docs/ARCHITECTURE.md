# Architecture

## Purpose

AI Logix is a logistics operations application for tracking delivery events, order state, photographic evidence, OCR/AI extraction, human review, authentication, roles, and audit activity.

## High-Level Architecture

```text
React/Vite frontend
  -> HTTP API with bearer JWT
FastAPI backend
  -> SQLAlchemy
PostgreSQL

FastAPI also serves local uploads from backend/uploads.
OCR runs behind provider abstractions.
Human review is the trust boundary for OCR/AI output.
```

## Backend FastAPI

The backend initializes the FastAPI app, configures CORS from environment, mounts local uploads, registers routers, and creates database tables through SQLAlchemy metadata.

Known routers:

- Main operations routes.
- Auth routes.
- Human review routes.
- User management routes.

## Frontend React/Vite

The frontend is a React/Vite app using Axios for API calls, TailwindCSS for styling, and Leaflet for map display. It includes auth context and protected route components.

## PostgreSQL

PostgreSQL stores users, drivers, stores, delivery events, order states, and audit logs. The current schema is defined through SQLAlchemy models.

## Docker Compose

Docker Compose runs:

- `db`: PostgreSQL 16.
- `backend`: FastAPI app on port `8000`.
- `frontend`: Vite app on port `5173`.

## Uploads

Evidence is stored locally under `backend/uploads`. FastAPI mounts uploads as static files. This is acceptable for local development but requires an access-control decision before production.

## OCR Provider Strategy

OCR/AI is decoupled through provider classes under `backend/app/services/ocr_providers/`.

Current provider posture:

- Mock provider: local deterministic development/testing.
- OpenAI provider: prepared for external AI extraction when configured.

## Human Review

Human review is mandatory as the trust boundary for AI-extracted data. OCR/AI output must not become final operational truth without supervisor/admin confirmation.

## Auth/RBAC

Authentication uses JWT bearer tokens. Authorization is enforced with backend dependencies:

- `require_admin`
- `require_supervisor_or_admin`
- `require_driver_or_above`

Roles:

- `ADMIN`
- `SUPERVISOR`
- `DRIVER`

## AuditLog

`audit_logs` records selected actions including login success/failure, evidence upload, OCR processing, review decisions, user creation, and user deactivation.

## Basic Flow

1. User logs in and receives JWT.
2. Driver/supervisor/admin creates delivery event or uploads evidence.
3. Evidence upload creates a delivery event.
4. Supervisor/admin processes OCR.
5. Supervisor/admin confirms or rejects review.
6. Trusted order state is updated only through approved workflow.
7. Important actions are logged.

## Current Limitations

- No formal migrations.
- Local evidence storage only.
- `/uploads` exposure requires production access policy.
- Login lacks rate limiting.
- Dependency versions are not fully pinned.
- No CI/CD pipeline.
- No production observability.
- No official order status taxonomy.
- No human review SLA.

## Next Improvements

Recommended next phase: Fase 1 - Seguridad, configuracion y secretos.

Priority improvements:

- Secret scanning.
- Environment separation.
- Strong production secret policy.
- Login rate limiting.
- Upload access hardening.
- CORS hardening.
- Migration strategy.
- CI validation gates.
