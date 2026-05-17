# Project State

## Project

AI Logix

## Last Updated

2026-05-17

## Current Phase

Fase 4 - Permisos DRIVER reales y asignacion operativa

## Status

Completed for driver ownership and operational assignment scope. `User.driver_id` is now the formal user-to-driver relationship, DRIVER operational actions are scoped to the assigned driver, and elevated roles keep global operational control.

## Detected Stack

- Backend: FastAPI, SQLAlchemy, Pydantic settings, Pytest.
- Database: PostgreSQL through Docker Compose.
- Frontend: React, Vite, TailwindCSS, Axios, Leaflet, Vitest, Testing Library.
- Auth: JWT bearer tokens.
- RBAC: `ADMIN`, `SUPERVISOR`, `DRIVER`.
- Evidence: local upload storage under `backend/uploads`.
- OCR/AI: provider strategy with mock and OpenAI provider.
- Audit: `audit_logs` table.

## Phase 0 Work Completed

- Created canonical agent operating standard in `AGENTS.md`.
- Created thin adapters in `CODEX.md` and `CLAUDE.md`.
- Added `.gitignore` coverage for secrets, generated files, uploads, logs, and build artifacts.
- Sanitized `.env.example` with development placeholders only.
- Removed `.env` and tracked Python bytecode artifacts from the Git index while preserving local files.
- Created planning memory: state, decisions, domain, risks, questions, inventory, metrics, maturity model, adoption map, tagging, automation, deprovisioning, and continuous improvement.
- Created sprint handoff folder for `000-foundation-metrics`.
- Created docs for architecture, data model, API, permissions, validation, operations, metrics, and Phase 0 audit.

## Acceptance Status

All required Phase 0 acceptance criteria are complete as documented in `planning/sprints/000-foundation-metrics/acceptance.md`.

All required Phase 1 acceptance criteria are complete as documented in `planning/sprints/001-security-configuration/acceptance.md`.

All required Phase 2 acceptance criteria are complete as documented in `planning/sprints/002-alembic-data-model/acceptance.md`.

All required Phase 3 acceptance criteria are complete as documented in `planning/sprints/003-critical-tests/acceptance.md`.

All required Phase 4 acceptance criteria are complete as documented in `planning/sprints/004-driver-permissions/acceptance.md`.

## Validation Status

- `docker compose config`: passed.
- `docker compose up --build -d`: passed; local containers started.
- `python -m pytest backend/tests/test_config_security.py`: passed in Fase 1.
- `python -m pytest backend/tests/test_alembic_config.py`: passed, 3 tests.
- `python -m pytest backend/tests`: passed, 66 tests in Fase 4.
- `docker compose exec backend python -m pytest`: passed, 66 tests in Fase 4.
- `cd frontend; npm install`: passed after correcting unavailable test dependency version.
- `cd frontend; npm run test`: passed, 9 tests in Fase 4.
- `cd frontend; npm run build`: passed.
- `cd frontend; npm run lint`: passed.
- `cd backend; python -m alembic -c alembic.ini history`: passed.
- `docker compose exec backend alembic -c alembic.ini history`: passed.
- `docker compose exec backend alembic -c alembic.ini current`: initially showed no revision because the local DB predated Alembic; after baseline adoption it reports `20260517_0002 (head)`.
- `docker compose exec backend alembic -c alembic.ini upgrade head`: initially blocked by duplicate table `drivers`; local baseline was adopted with `stamp 20260517_0001`, then upgrade to `20260517_0002` passed.
- Required file existence: passed.
- Empty required file check: passed.
- Placeholder search in Phase 2 files: passed.
- Fase 3 warning noise remains: backend local emitted 235 warnings and Docker emitted 173 warnings, primarily Pydantic class Config and `datetime.utcnow` deprecations.
- Fase 4 local backend warning noise: 316 warnings, primarily existing deprecations.
- Fase 4 Docker backend warning noise: 240 warnings, primarily existing deprecations.

## Blockers

No blockers remain for closing Phase 4 after final validation commands are recorded. CI/CD automation, evidence protection, retention, and driver UX remain future work.

## Open Risks

- Formal Alembic baseline exists, but existing databases created before Alembic may need `alembic stamp head`.
- Development defaults are blocked outside development for critical settings, but actual secret management and rotation process still need CI/deployment integration.
- `/uploads` is served by FastAPI and needs production access policy.
- Login lacks rate limiting.
- Evidence retention is undefined.
- CI/CD is missing.
- Order status taxonomy is not formalized.
- Human review SLA is undefined.
- Backend warning noise is high and should be reduced.
- CI/CD does not run the new test suite automatically.
- Frontend tests mock Leaflet and do not replace browser/E2E validation.
- Existing DRIVER users may need `driver_id` backfill.
- Historical events may have null `driver_id`.
- Driver authorization is based on `driver_id`, not formal order/route assignment.

## Recommended Next Phase

Fase 5 - Evidencia protegida y politica de retencion.

Recommended focus:

- Protect evidence access behind authorization.
- Define evidence retention/archive/delete policy.
- Prevent unrestricted `/uploads` exposure in non-local environments.
- Keep driver ownership tests passing while securing evidence delivery.
