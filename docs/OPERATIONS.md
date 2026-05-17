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

## Healthcheck

```bash
curl http://localhost:8000/api/health
```

Expected result: backend returns status ok.

## Backend Tests

```bash
docker compose exec backend pytest
```

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
- Do not trust OCR/AI output without human review.

## Checklist Before Demo

- `docker compose config` passes.
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
