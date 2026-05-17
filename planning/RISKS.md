# Risks

| Risk | Likelihood | Impact | Severity | Mitigation | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- |
| Migracion baseline puede diferir de una DB existente creada con `create_all`. | Medium | Alembic may see objects already present and require stamping instead of applying baseline. | High | For existing DBs, inspect schema and use `alembic stamp head` only after confirming it matches baseline. | Engineering/DevOps | Open |
| Secretos default en desarrollo. | Medium | Defaults can be copied into staging/production. | High | Runtime settings now block unsafe defaults outside development; keep `.env` out of Git and rotate all secrets before non-local environments. | Engineering/Security | Mitigated |
| Posible exposicion de `/uploads`. | Medium | Evidence photos may be accessible without adequate production controls. | High | Define evidence access model, avoid public serving in production, add authorization gate before production. | Security/Engineering | Open |
| Existing `DRIVER` users may not have `driver_id`. | Medium | Existing driver accounts can be blocked from operational actions after Fase 4. | Medium | Assign valid `driver_id` before using DRIVER accounts in shared environments. | Ops/Engineering | Open |
| Login sin rate limit. | Medium | Brute-force attempts can target credentials. | High | Add rate limiting and lockout/monitoring strategy in a future security phase. | Security | Open |
| OCR can fail or return low-confidence output. | High | Review queue may receive incomplete or wrong data. | Medium | Keep human review mandatory; track OCR failure and confidence metrics. | Engineering/Ops | Open |
| Evidence files can grow without retention policy. | High | Disk usage, privacy, and operational cost risk. | High | Define retention, archival, and deletion policy before production. | Ops/Security | Open |
| Backend dependencies are not fully pinned. | Medium | Builds can drift over time. | Medium | Pin dependencies and add dependency update workflow. | Engineering | Open |
| Falta pipeline CI/CD. | High | Regressions may ship manually. | High | Add CI for compose config, backend tests, frontend build/lint, and secret scan. | DevOps | Open |
| Falta documentacion de estados validos de orden. | High | Reporting and workflows can diverge. | Medium | Product/Ops must define canonical status taxonomy. | Product/Ops | Open |
| Falta definicion de SLA de revision humana. | High | Pending reviews may block trusted state updates. | Medium | Define SLA and metric target for review queue. | Product/Ops | Open |
| Audit logging is minimal. | Medium | Sensitive changes may lack enough forensic detail. | Medium | Expand audit action coverage and retention policy. | Security/Engineering | Open |
| No production backup/restore procedure. | Medium | Data loss risk in real operations. | High | Define backup, restore, and recovery objectives before production. | DevOps/Ops | Open |
| Secret scanning is not automated in CI/CD. | Medium | Secrets may be committed if local review fails. | High | Add secret scan to CI and optionally pre-commit in a future phase. | Security/DevOps | Open |
| Full runtime stack was not rebuilt during Fase 1. | Low | Runtime integration issues may remain until demo/next implementation validation. | Medium | `docker compose config` and config tests passed; run `docker compose up --build` before demo or Fase 2 closure. | Engineering | Open |
| Pydantic class-based `Config` deprecation warnings. | Medium | Future Pydantic major version may require config migration. | Low | Migrate settings/schemas to `ConfigDict` in a future maintenance sprint. | Engineering | Open |
| Flexible JSON fields can make validation and reporting harder. | High | OCR/review payloads may drift by provider or workflow. | Medium | Keep current JSON fields but document expected shapes before analytics/reporting hardening. | Engineering/Product | Open |
| Downgrade support can be limited for future data-changing migrations. | Medium | Rollback may not restore transformed/deleted data. | High | Require backup and explicit rollback notes before destructive migrations. | DevOps/Engineering | Open |
| Migrations are not automated in CI/CD. | High | Migration drift may be missed before merge/deploy. | High | Add CI checks in a future phase for migration history and tests. | DevOps | Open |
| Backup/restore is not implemented. | Medium | Production migration rollback may be unsafe. | High | Define backup/restore before production migrations. | DevOps/Ops | Open |
| Suite backend can diverge from PostgreSQL behavior. | Medium | SQLite in-memory tests may miss PostgreSQL-specific issues. | Medium | Keep Docker/PostgreSQL smoke validation and add DB-specific tests in future CI. | Engineering/QA | Open |
| Frontend tests mock Leaflet. | Medium | Map rendering issues may not be caught by component tests. | Low | Add targeted browser/E2E smoke later if map UX becomes critical. | Frontend Engineering | Open |
| Critical coverage is not full coverage. | High | Untested secondary flows can still regress. | Medium | Expand tests by risk in future sprints. | Engineering/QA | Open |
| Warning noise remains high. | High | Real warnings can be missed among deprecation noise. | Medium | Migrate Pydantic Config and UTC timestamp usage in a maintenance sprint. | Engineering | Open |
| OCR confirm action lacks explicit AuditLog coverage. | Medium | Some OCR confirmation decisions may be harder to trace. | Medium | Decide whether `OCR_CONFIRMED` should be logged in a future audit hardening phase. | Security/Engineering | Open |
| CI/CD does not run the new suite automatically. | High | Regressions can still merge if commands are skipped manually. | High | Add GitHub Actions or equivalent in a future CI/CD phase. | DevOps | Open |
| Historical delivery events may have `driver_id` null. | High | Old events may not map to a driver user for ownership reporting. | Medium | Preserve historical data and backfill only after business review. | Product/Engineering | Open |
| Orders do not have formal driver assignment. | High | Driver ownership is enforced by event/evidence `driver_id`, not by an order assignment table. | High | Define order assignment model in a future workflow/data phase. | Product/Engineering | Open |
| No dedicated DRIVER order-state endpoint exists. | Medium | Driver UI cannot yet show scoped order state from backend endpoint. | Medium | Add scoped driver endpoint when driver workflow UX is implemented. | Product/Engineering | Open |
| Fase 4 ownership is driver-based, not route-based. | Medium | Route or stop-level authorization remains undefined. | Medium | Add route/manifest rules after operations defines assignment model. | Product/Ops | Open |
| Mobile-first DRIVER experience is still missing. | High | Driver workflow remains limited for field use. | Medium | Plan a later mobile-first driver phase. | Product/Frontend | Open |

## Review Cadence

Review risks at sprint start, sprint close, before demo, and before production release.
