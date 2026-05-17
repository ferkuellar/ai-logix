# Testing

## Objetivo

La estrategia de pruebas de AI Logix protege los flujos criticos actuales: auth, permisos, evidencia, OCR mock, revision humana, AuditLog, configuracion segura, migraciones y shell frontend. Fase 3 prioriza regresion critica sobre porcentaje de cobertura.

## Tipos de pruebas

| Type | Scope | Tooling |
| --- | --- | --- |
| Backend unit/integration-lite | FastAPI routes, services, auth, DB models through SQLite in-memory. | `pytest`, `TestClient` |
| Frontend component tests | App shell, login, auth/localStorage, dashboard with mocked API. | Vitest, Testing Library, jsdom |
| Validation/manual smoke | Docker Compose, build, lint, runtime checks. | Docker Compose, npm, curl/manual |

## Backend Tests

Run locally from repo root:

```bash
python -m pytest backend/tests
```

Run inside Docker:

```bash
docker compose exec backend python -m pytest
```

The direct command below may fail in the current container because import path can omit `/app`:

```bash
docker compose exec backend pytest
```

Use `python -m pytest` as the canonical Docker command.

## Frontend Tests

Install dependencies:

```bash
cd frontend
npm install
```

Run tests:

```bash
npm run test
```

Watch mode:

```bash
npm run test:watch
```

## Build And Lint

```bash
cd frontend
npm run build
npm run lint
```

## Local Environment

Backend tests set test environment variables in `backend/tests/conftest.py`:

- `DATABASE_URL=sqlite+pysqlite:///:memory:`
- `OCR_PROVIDER=mock`
- test-only JWT settings

This keeps tests isolated from local PostgreSQL and external OCR.

## Test Users And Roles

`backend/tests/conftest.py` creates users by role:

- `ADMIN`
- `SUPERVISOR`
- `DRIVER`

Helpers create authenticated clients with bearer tokens for each role.

## OCR / IA Mocking

Tests force `OCR_PROVIDER=mock`. No test should call OpenAI or require `OPENAI_API_KEY`.

## Upload Handling

Upload tests use small in-memory PNG bytes. The global backend fixture removes `backend/uploads/evidence` before and after each test to avoid leftover evidence files.

## Frontend API Mocking

Frontend tests mock `frontend/src/api/client.js` functions. Dashboard tests mock `/api/order-states` through `fetchOrderStates`. Leaflet is mocked because map rendering is not the target of Fase 3 component tests.

## What Fase 3 Does Not Cover

- Full browser E2E flows.
- Real PostgreSQL migration application.
- Real OpenAI OCR.
- Production file storage.
- Protected evidence access.
- CI/CD automation.
- Complete code coverage.

## Troubleshooting

| Symptom | Likely Cause | Action |
| --- | --- | --- |
| `ModuleNotFoundError: No module named 'app'` in Docker pytest | Direct `pytest` command path issue. | Use `docker compose exec backend python -m pytest`. |
| Frontend tests fail on Leaflet DOM APIs | jsdom does not provide map browser APIs. | Mock `react-leaflet` in component tests. |
| Upload tests leave files | Fixture cleanup did not run or process interrupted. | Delete `backend/uploads/evidence` locally if needed. |
| Pydantic deprecation warnings | Current schemas/settings use class-based Config. | Track for maintenance sprint. |

## Sprint Close Checklist

- `docker compose config` passes.
- `python -m pytest backend/tests` passes.
- `docker compose exec backend python -m pytest` passes when Docker is running.
- `cd frontend && npm run test` passes.
- `cd frontend && npm run build` passes.
- `cd frontend && npm run lint` passes.
- `docs/VALIDATION.md` records results and warnings.
- `planning/RISKS.md` records residual risks.
