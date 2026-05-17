# Sprint 002 Blueprint - Alembic Data Model

## Archivos a revisar

- `AGENTS.md`
- `README.md`
- `docker-compose.yml`
- `backend/requirements.txt`
- `backend/app/main.py`
- `backend/app/db/base.py`
- `backend/app/db/session.py`
- `backend/app/core/config.py`
- `backend/app/models/`
- `docs/DATA_MODEL.md`
- `docs/OPERATIONS.md`
- `docs/VALIDATION.md`
- `planning/STATE.md`
- `planning/DECISIONS.md`
- `planning/RISKS.md`
- `planning/METRICS.md`

## Archivos a crear

- `backend/alembic.ini`
- `backend/alembic/env.py`
- `backend/alembic/script.py.mako`
- `backend/alembic/versions/20260517_0001_baseline_schema.py`
- `backend/tests/test_alembic_config.py`
- `docs/DATABASE_MIGRATIONS.md`
- `docs/auditoria-fase-2-alembic-data-model.md`
- `planning/sprints/002-alembic-data-model/requirements.md`
- `planning/sprints/002-alembic-data-model/blueprint.md`
- `planning/sprints/002-alembic-data-model/acceptance.md`
- `planning/sprints/002-alembic-data-model/handoff-prompt.md`

## Archivos a modificar

- `backend/requirements.txt`
- `backend/app/main.py`
- `docs/DATA_MODEL.md`
- `docs/OPERATIONS.md`
- `docs/VALIDATION.md`
- `docs/METRICS.md`
- `planning/STATE.md`
- `planning/DECISIONS.md`
- `planning/RISKS.md`
- `planning/QUESTIONS.md`
- `planning/METRICS.md`
- `README.md`

## Plan tecnico paso a paso

1. Run Fase 0/Fase 1 precheck.
2. Inspect current models and DB setup.
3. Add Alembic dependency.
4. Create Alembic config under `backend/`.
5. Configure `env.py` to load `settings.database_url` and model metadata.
6. Create baseline migration manually reviewed against current models.
7. Restrict `create_all` to development compatibility.
8. Add structural tests for Alembic files and metadata.
9. Update migration and data model docs.
10. Run validation and document any skipped Docker runtime checks.
11. Update sprint acceptance and audit.

## Estrategia de validacion

- `docker compose config`
- `python -m pytest backend/tests/test_alembic_config.py`
- `python -m pytest backend/tests`
- `cd backend && python -m alembic -c alembic.ini history` when Alembic is installed.
- `cd backend && python -m alembic -c alembic.ini current` when database is reachable.
- `cd backend && python -m alembic -c alembic.ini upgrade head` when database is reachable.

## Estrategia de rollback

- Revert Alembic files if not applied.
- If baseline was applied locally, downgrade with `alembic downgrade base` or reset local DB volume intentionally.
- Do not edit applied shared migrations; create a new migration to correct schema.

## Riesgos

- Baseline may differ from already-created local DBs if manual schema drift exists.
- Existing DBs may need `alembic stamp head`.
- Downgrade is safe only for empty/local schemas; data-bearing rollback needs backups.

## No-go items

- No model redesign.
- No business-rule changes.
- No data deletion.
- No automatic migration-on-start entrypoint.
- No cloud resources.
