# Operations

## Local Environment Setup

1. Create local environment file:

   ```bash
   cp .env.example .env
   ```

2. Replace local values in `.env` as needed. Do not commit `.env`.

3. Validate Compose:

   ```bash
   docker compose config
   ```

4. Start the stack:

   ```bash
   docker compose up --build
   ```

## Seed Admin

```bash
docker compose exec backend python -m app.scripts.seed_admin
```

Use development-only credentials from local `.env`. Rotate before any shared environment.

## Non-Development Configuration

For any environment where `APP_ENV` is not `development`, configure:

- `DATABASE_URL` with the target database URL.
- `SECRET_KEY` with a random value at least 32 characters long.
- `SEED_ADMIN_PASSWORD` with a non-default value at least 12 characters long.
- `CORS_ORIGINS` with explicit origins, never `*`.

The backend fails at startup if these settings are unsafe. Expected error examples:

```text
Unsafe production configuration: SECRET_KEY must be changed for non-development environments.
Unsafe production configuration: SEED_ADMIN_PASSWORD must be changed for non-development environments.
Unsafe production configuration: CORS_ORIGINS cannot include '*' for non-development environments.
```

The error names the unsafe setting but does not print secret values.

## Healthcheck

```bash
curl http://localhost:8000/api/health
```

Expected result: backend returns status ok.

## Backend Tests

```bash
docker compose exec backend pytest
```

## Database Migrations

Alembic is configured under `backend/`.

Check migration state:

```bash
docker compose exec backend alembic -c alembic.ini current
docker compose exec backend alembic -c alembic.ini history
```

Apply migrations:

```bash
docker compose exec backend alembic -c alembic.ini upgrade head
```

Create a new migration after model changes:

```bash
docker compose exec backend alembic -c alembic.ini revision --autogenerate -m "describe change"
```

Rollback the last migration locally:

```bash
docker compose exec backend alembic -c alembic.ini downgrade -1
```

Review `docs/DATABASE_MIGRATIONS.md` before applying migrations to shared environments.

## Frontend Build And Lint

```bash
cd frontend
npm install
npm run build
npm run lint
```

## Logs

```bash
docker compose logs backend
docker compose logs frontend
docker compose logs db
```

## Controlled Local Reset

Stop services without deleting volume data:

```bash
docker compose down
```

Delete local database volume intentionally:

```bash
docker compose down -v
```

Use volume deletion only when local data loss is acceptable.

## Production Prohibitions

- Do not use `.env.example` values in production.
- Do not expose `/uploads` without an approved access-control model.
- Do not use local filesystem evidence storage as final production storage without a retention/backup decision.
- Do not run seed admin with shared default credentials in production.
- Do not deploy without secret rotation.
- Do not deploy without database backup/restore plan.
- Do not apply production migrations without backup and manual review.
- Do not trust OCR/AI output without human review.

## Checklist Before Demo

- `docker compose config` passes.
- Security config tests pass.
- `docker compose up --build` starts all services.
- Admin seed works with demo-only credentials.
- Frontend opens at `http://localhost:5173`.
- Backend health passes.
- Login works.
- Driver upload flow works with non-private sample evidence.
- OCR mock flow works.
- Human review confirm/reject works.
- No real secrets or private evidence are used.
- Risks and limitations are disclosed.
