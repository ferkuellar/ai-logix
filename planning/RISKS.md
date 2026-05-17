# Risks

| Risk | Likelihood | Impact | Severity | Mitigation | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- |
| Falta de migraciones formales o migraciones por validar. | High | Schema changes can become unsafe or inconsistent. | High | Add Alembic or equivalent migration workflow in Phase 1/2 before production. | Engineering | Open |
| Secretos default en desarrollo. | Medium | Defaults can be copied into staging/production. | High | Runtime settings now block unsafe defaults outside development; keep `.env` out of Git and rotate all secrets before non-local environments. | Engineering/Security | Mitigated |
| Posible exposicion de `/uploads`. | Medium | Evidence photos may be accessible without adequate production controls. | High | Define evidence access model, avoid public serving in production, add authorization gate before production. | Security/Engineering | Open |
| `DRIVER` user has no strong enforced relationship with `Driver` domain record. | Medium | A driver user could submit events not tied to an assigned driver identity. | Medium | Define user-driver relationship and assignment rules in a future sprint. | Product/Engineering | Open |
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

## Review Cadence

Review risks at sprint start, sprint close, before demo, and before production release.
