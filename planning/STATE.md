# Project State

## Project

AI Logix

## Last Updated

2026-05-17

## Current Phase

Fase 3 - Tests criticos backend/frontend

## Status

Completed for critical backend/frontend regression scope. The backend now has 49 passing tests covering health, auth, permissions, evidence, OCR, review, AuditLog, config, and Alembic. The frontend now has Vitest/Testing Library coverage for app render, login, auth/localStorage, and dashboard API mocking.

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

## Validation Status

- `docker compose config`: passed.
- `docker compose up --build -d`: passed; local containers started.
- `python -m pytest backend/tests/test_config_security.py`: passed in Fase 1.
- `python -m pytest backend/tests/test_alembic_config.py`: passed, 3 tests.
- `python -m pytest backend/tests`: passed, 49 tests in Fase 3.
- `docker compose exec backend python -m pytest`: passed, 49 tests in Fase 3.
- `cd frontend; npm install`: passed after correcting unavailable test dependency version.
- `cd frontend; npm run test`: passed, 8 tests.
- `cd frontend; npm run build`: passed.
- `cd frontend; npm run lint`: passed.
- `cd backend; python -m alembic -c alembic.ini history`: passed.
- `docker compose exec backend alembic -c alembic.ini history`: passed.
- `docker compose exec backend alembic -c alembic.ini current`: passed with no revision displayed because the local DB is not stamped.
- `docker compose exec backend alembic -c alembic.ini upgrade head`: executed and blocked by duplicate table `drivers` because the existing local DB already had tables from development `create_all`; baseline adoption is documented.
- Required file existence: passed.
- Empty required file check: passed.
- Placeholder search in Phase 2 files: passed.
- Fase 3 warning noise remains: backend local emitted 235 warnings and Docker emitted 173 warnings, primarily Pydantic class Config and `datetime.utcnow` deprecations.

## Blockers

No blockers remain for closing Phase 3. CI/CD automation and warning reduction remain future work.

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

## Recommended Next Phase

Fase 4 - Permisos DRIVER reales y asignacion operativa.

Recommended focus:

- Define formal `User` to `Driver` relationship.
- Enforce driver ownership/assignment for operational actions.
- Clarify which driver can create/update events for each order.
- Keep current critical tests passing while hardening permissions.
