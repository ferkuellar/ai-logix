# AI Logix - Agent Operating Standard

## Project

Name: AI Logix

Purpose: AI Logix is a logistics operations system for tracking delivery events, order state, photographic evidence, OCR/AI extraction, human review, authentication, roles, and audit visibility. The system is already implemented as an existing repository; agents must improve and operate it, not recreate it.

## Current Detected Stack

- Backend: FastAPI, SQLAlchemy, Pydantic settings, Python.
- Database: PostgreSQL.
- Local runtime: Docker Compose.
- Frontend: React, Vite, TailwindCSS, Axios, Leaflet.
- Authentication: JWT bearer tokens.
- Authorization: roles `ADMIN`, `SUPERVISOR`, `DRIVER`.
- Evidence: local upload storage under `backend/uploads`.
- OCR/AI: provider abstraction with mock and OpenAI provider support.
- Audit: `audit_logs` table.
- Tests: Pytest backend tests; frontend build/lint scripts.

## Architect / Builder Model

- Architect work defines scope, requirements, blueprint, risks, metrics, and acceptance.
- Builder work implements only the approved sprint scope.
- Builder must not redefine product scope.
- Builder must not invent business rules.
- Builder must raise missing business decisions as questions in `planning/QUESTIONS.md`.
- Builder must record durable technical decisions in `planning/DECISIONS.md`.

## Handoff Rule

The handoff is the folder, not the conversation. Chat context can help orientation, but repository artifacts are authoritative.

## Mandatory Reading Order

Future agents must read in this order:

1. `AGENTS.md`
2. `planning/STATE.md`
3. `planning/DECISIONS.md`
4. `planning/DOMAIN.md`
5. `planning/RISKS.md`
6. `planning/METRICS.md`
7. `planning/sprints/current-sprint/`
8. `docs/`

For the current sprint, `planning/sprints/current-sprint/` maps to `planning/sprints/000-foundation-metrics/`.

## Builder Rules

- Work inside the existing repository.
- Do not create nested repositories such as `ai-logix/ai-logix`.
- Read an existing file before modifying it.
- Preserve useful content when improving documents.
- Keep changes scoped to the active sprint.
- Do not move backend, frontend, docs, or Docker files unless a sprint explicitly requires it.
- Do not modify application code during documentation-only phases.
- Validate against the active sprint `acceptance.md`.
- Report files created, files modified, validations run, skipped validations, and risks.
- Update `planning/STATE.md` when project state changes.
- Update `planning/DECISIONS.md` when a durable decision is made.
- Update `planning/RISKS.md` when a risk is discovered or mitigated.
- Update `planning/QUESTIONS.md` when a required business answer is missing.

## Security Rules

- Never commit `.env`.
- Never store real API keys, tokens, passwords, private URLs, or production secrets.
- Keep secrets in environment variables or managed secret stores.
- Treat uploaded evidence as sensitive operational data.
- Do not expose uploaded evidence publicly in production without an approved access model.
- Enforce authorization in the backend.
- Rotate local/default secrets before staging or production.
- Do not use AI/OCR output as operational truth without human review.
- Document security risks instead of hiding them.

## Documentation Rules

- Every sprint must include:
  - `requirements.md`
  - `blueprint.md`
  - `acceptance.md`
  - `handoff-prompt.md`
- Every durable decision belongs in `planning/DECISIONS.md`.
- Every visible risk belongs in `planning/RISKS.md`.
- Every missing business answer belongs in `planning/QUESTIONS.md`.
- Every important metric must be measurable, auditable, or documented as not yet instrumented.
- Avoid empty, generic, or placeholder-only documents.
- Do not leave unresolved placeholders; convert uncertainty into a question or a documented risk.

## Validation Rules

Use the strongest practical validation for the change:

- Documentation-only changes:
  - Confirm required files exist.
  - Confirm no required file is empty.
  - Search for unresolved placeholders.
  - Run `docker compose config`.
- Backend changes:
  - Run backend tests with `pytest`.
  - Validate auth, role, upload, OCR, review, and audit flows affected by the change.
- Frontend changes:
  - Run `npm run build`.
  - Run `npm run lint`.
- Runtime changes:
  - Run `docker compose up --build` when feasible.

If a validation cannot run, document command, error, probable cause, impact, and next action in `docs/VALIDATION.md` and the sprint acceptance file.

## Main Commands

```bash
docker compose config
docker compose up --build
docker compose exec backend pytest
docker compose exec backend python -m app.scripts.seed_admin
cd frontend
npm install
npm run build
npm run lint
```

## Definition Of Done

A sprint is done only when:

- Scope matches the sprint requirements.
- Acceptance criteria are checked only when true.
- Required docs are updated.
- Decisions, risks, questions, and metrics are current.
- Validation is executed or skipped with a documented reason and impact.
- No secrets are introduced.
- No required file is empty.
- No unjustified placeholder remains.
- Next phase or next sprint recommendation is explicit.

## Phase 0 Prohibitions

During Phase 0:

- Do not create a new project.
- Do not create `ai-logix/ai-logix`.
- Do not delete backend, frontend, docs, or `docker-compose.yml`.
- Do not move application code.
- Do not implement WhatsApp.
- Do not implement S3/R2.
- Do not implement a mobile app.
- Do not implement route optimization.
- Do not add autonomous AI agents.
- Do not change business rules.
- Do not store real secrets.
- Do not commit `.env`.
