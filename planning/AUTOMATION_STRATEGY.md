# Automation Strategy

This file defines future automation without implementing it in Phase 0.

| Automation | Objective | Expected Command | When To Run | Current Status | Recommended Phase |
| --- | --- | --- | --- | --- | --- |
| Docker Compose config | Validate local orchestration syntax. | `docker compose config` | Every sprint and before demo. | Manual; passed in Phase 0. | Phase 0 complete |
| Backend tests | Validate API, auth, upload, OCR, review behavior. | `docker compose exec backend pytest` | Every backend change and CI. | Tests exist; not run in Phase 0 because app code did not change. | Phase 1 |
| Frontend build | Validate production frontend bundle. | `cd frontend && npm run build` | Every frontend change and CI. | Script exists; not run in Phase 0 because frontend code did not change. | Phase 1 |
| Frontend lint | Validate frontend code quality. | `cd frontend && npm run lint` | Every frontend change and CI. | Script exists; not run in Phase 0 because frontend code did not change. | Phase 1 |
| Migrations | Validate database schema evolution. | Future: `alembic upgrade head` | Every schema change and deploy. | Not implemented. | Phase 1 or 2 |
| Seed admin | Create local admin user. | `docker compose exec backend python -m app.scripts.seed_admin` | Local setup and demo reset. | Script exists. | Phase 1 |
| Healthcheck | Confirm backend availability. | `curl http://localhost:8000/api/health` | Startup, CI smoke, demo. | Endpoint exists; not automated. | Phase 1 |
| Secret scan | Prevent secret commits. | Future: `gitleaks detect` or equivalent. | Pre-commit and CI. | Not implemented; `.env` removed from index. | Phase 1 |
| Metrics report | Produce current Axon-AI metrics. | Future SQL/script from `planning/METRICS.md`. | Weekly and sprint close. | Metrics defined; reporting not automated. | Phase 2 |
| CI/CD | Gate changes before merge/deploy. | Future GitHub Actions workflow. | Pull requests and main branch. | Not implemented. | Phase 1 |

## Automation Guardrails

- Do not automate business-rule changes.
- Do not call real OCR/AI providers in CI by default.
- Do not seed production with demo credentials.
- Do not create cloud resources without owner, purpose, environment, and review date.
