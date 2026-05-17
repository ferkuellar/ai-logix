# Axon-AI Metrics

## Producto

| Name | Category | Purpose | Formula / Validation Method | Owner | Target | Current Baseline | Data Source | Frequency | Risk if Ignored |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `order_state_coverage` | Producto | Measure orders with trusted current state. | `count(order_states) / count(distinct delivery_events.order_number)` where order number exists. | Ops/Product | 95%+ once live | Not baselined; schema supports measurement. | PostgreSQL | Weekly | Orders may lack operational visibility. |
| `evidence_capture_rate` | Producto | Measure evidence adoption. | `PHOTO_UPLOADED events / delivery events requiring evidence`. | Ops | Target pending evidence policy | Not fully measurable until evidence rules are defined. | PostgreSQL | Weekly | Required evidence may be missing. |
| `human_review_pending_count` | Producto | Track review backlog. | Count reviewable OCR/evidence records pending review. | Supervisors | Pending target from SLA | Partially measurable via review service/database JSON. | PostgreSQL | Daily | AI-derived data can remain untrusted. |
| `human_review_sla_minutes` | Producto | Track review timeliness. | Minutes from OCR processed/upload to human decision. | Ops | Target pending SLA decision | Not instrumented. | Audit logs + delivery events | Daily | Review delays block trusted state. |
| `orders_without_current_status` | Producto | Identify orders lacking trusted status. | Distinct delivery event order numbers not present in `order_states`. | Ops | 0 for active orders | Measurable. | PostgreSQL | Weekly | Missing statuses reduce dashboard reliability. |

## Operacion

| Name | Category | Purpose | Formula / Validation Method | Owner | Target | Current Baseline | Data Source | Frequency | Risk if Ignored |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `api_health_status` | Operacion | Confirm backend responds. | `GET /api/health` returns status ok. | Engineering | 100% when environment is up | Endpoint exists; runtime not executed in Phase 0. | API | Daily/dev startup | Broken API may go unnoticed. |
| `backend_startup_success` | Operacion | Confirm backend starts. | Backend container starts without crash. | DevOps | 100% | Not executed in Phase 0. | Docker Compose | Per change | Runtime defects may block dev/demo. |
| `docker_compose_valid` | Operacion | Confirm compose file parses. | `docker compose config` exits 0. | DevOps | 100% | Passed on 2026-05-17. | CLI | Every sprint | Local environment can break. |
| `upload_success_rate` | Operacion | Track valid evidence uploads. | Successful upload responses / upload attempts. | Ops/Engineering | 98%+ after pilot | Not baselined. | API/audit logs | Weekly | Drivers may fail to capture evidence. |
| `upload_rejection_rate` | Operacion | Track rejected files. | Rejected upload attempts / upload attempts. | Engineering | Under agreed threshold | Not instrumented separately. | API logs/errors | Weekly | File validation friction may hurt adoption. |
| `api_error_rate` | Operacion | Track API health. | 5xx responses / total API responses. | Engineering | Under 1% | Not instrumented. | Future logs/monitoring | Daily in production | Production defects may persist. |

## Seguridad

| Name | Category | Purpose | Formula / Validation Method | Owner | Target | Current Baseline | Data Source | Frequency | Risk if Ignored |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `secrets_in_repo_count` | Seguridad | Detect committed secrets. | Secret scan findings count. | Security | 0 | `.env` removed from index; scan not automated. | Git/secret scan | Every PR | Secrets may leak. |
| `protected_endpoint_coverage` | Seguridad | Ensure sensitive endpoints require auth/roles. | Protected endpoints / endpoints requiring protection. | Engineering/Security | 100% | Documented for known endpoints. | Code review/tests | Every auth change | Broken access control. |
| `failed_login_count` | Seguridad | Track suspicious auth failures. | Count `LOGIN_FAILED` audit logs. | Security/Ops | Alert threshold pending | Measurable. | `audit_logs` | Daily in production | Brute force may go unnoticed. |
| `audit_log_critical_action_coverage` | Seguridad | Ensure critical actions are audited. | Audited critical actions / defined critical actions. | Security | 100% after critical-action list exists | Partial. | Code + `audit_logs` | Sprint close | Forensics gaps. |
| `default_secret_detected` | Seguridad | Detect unsafe config. | Check `.env`/runtime values for known defaults. | Security/DevOps | False | `.env.example` intentionally contains sample placeholders; runtime not scanned. | Config/secret scan | Every deploy | Default credentials can reach production. |
| `env_example_completeness` | Seguridad | Ensure environment template documents required settings. | Required variables present in `.env.example` / required variables list. | Engineering/DevOps | 100% | 100% for Fase 1 required variables. | File review | Every config change | Missing variables slow setup or cause unsafe defaults. |
| `unsafe_production_config_blocked` | Seguridad | Confirm unsafe non-development config fails fast. | Config tests for production/default secret/default seed/missing DB/wildcard CORS. | Security/Engineering | True | True; tests added in Fase 1. | Pytest | Every config change | Unsafe deployments may start. |
| `cors_wildcard_blocked` | Seguridad | Confirm wildcard CORS is rejected outside development. | Config test with `APP_ENV=production` and `CORS_ORIGINS=*`. | Security/Engineering | True | True; test added in Fase 1. | Pytest | Every config change | Cross-origin exposure can expand unexpectedly. |
| `config_security_tests_passed` | Seguridad | Track security config test health. | `python -m pytest backend/tests/test_config_security.py` exits 0. | Engineering/QA | 100% | 100%; 7/7 passed in Fase 1. | Pytest | Every config change | Config regressions can ship. |

## OCR / IA

| Name | Category | Purpose | Formula / Validation Method | Owner | Target | Current Baseline | Data Source | Frequency | Risk if Ignored |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `ocr_processed_count` | OCR / IA | Count OCR processing volume. | Count `OCR_PROCESSED` audit events. | Ops/Engineering | Baseline after pilot | Measurable. | `audit_logs` | Weekly | OCR usage is invisible. |
| `ocr_failed_count` | OCR / IA | Track OCR failures. | Count OCR errors once logged. | Engineering | 0 critical failures | Not explicitly instrumented. | Future logs/audit | Weekly | OCR reliability issues remain hidden. |
| `ocr_confidence_average` | OCR / IA | Measure extraction quality. | Average confidence from provider output if available. | Product/Ops | Target pending provider schema | Not available in verified model. | OCR provider output | Weekly | Low-quality extraction may be trusted accidentally. |
| `ocr_human_review_required_rate` | OCR / IA | Confirm AI output goes through review. | Review-required OCR outputs / OCR outputs. | Security/Ops | 100% | Policy documented; measurement partial. | DB/audit logs | Weekly | AI may bypass human control. |
| `ocr_confirmed_rate` | OCR / IA | Track accepted OCR output. | Confirmed reviews / processed OCR events. | Ops | Baseline after pilot | Measurable via audit logs. | `audit_logs` | Weekly | Poor extraction quality may go unnoticed. |
| `ocr_rejected_rate` | OCR / IA | Track rejected OCR output. | Rejected reviews / processed OCR events. | Ops | Baseline after pilot | Measurable via audit logs. | `audit_logs` | Weekly | Model/provider issues may persist. |

## Calidad

| Name | Category | Purpose | Formula / Validation Method | Owner | Target | Current Baseline | Data Source | Frequency | Risk if Ignored |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `backend_test_pass_rate` | Calidad | Track backend correctness. | Passing pytest tests / total pytest tests. | Engineering/QA | 100% | 100%; 49/49 passed locally and in Docker in Fase 3. | Pytest | Every backend change | Regressions can ship. |
| `frontend_build_success` | Calidad | Confirm frontend compiles. | `npm run build` exits 0. | Frontend Engineering | 100% | Passed in Fase 1. | npm/Vite | Every frontend change | Broken UI build. |
| `frontend_lint_success` | Calidad | Confirm frontend lint health. | `npm run lint` exits 0. | Frontend Engineering | 100% | Passed in Fase 1. | npm/ESLint | Every frontend change | Maintainability defects accumulate. |
| `migration_status` | Calidad | Track schema-change safety. | Migration tool present and baseline migration exists. | Engineering/DevOps | Alembic configured with baseline | Alembic baseline added in Fase 2. | Repo/DB | Every schema change | Unsafe schema evolution. |
| `docs_completeness_score` | Calidad | Measure required docs coverage. | Existing required docs / required docs. | Architecture/PM | 100% for Phase 0 | 100% for required Phase 0 docs. | File check | Sprint close | Future builders lack context. |
| `migration_head_current` | Database | Confirm database is at Alembic head. | `alembic current` equals latest `alembic heads`. | Engineering/DevOps | Current equals head | Docker command executed; existing local DB is unstamped because tables predate Alembic. | Alembic/PostgreSQL | Every deploy | App may run against stale schema. |
| `schema_baseline_created` | Database | Confirm baseline migration exists. | Baseline file present with expected tables. | Engineering | True | True in Fase 2. | Repo | Sprint close | Future migrations lack starting point. |
| `alembic_history_available` | Database | Confirm migration history is readable. | `alembic history` exits 0. | Engineering/DevOps | True | True; passed locally and in Docker in Fase 2. | Alembic | Every schema change | Migration lineage may be broken. |
| `create_all_restricted` | Database | Confirm automatic schema creation is not used outside development. | Code review of `backend/app/main.py`. | Engineering | True | True in Fase 2. | Code review | Every startup/schema change | Non-local schema can drift outside migrations. |
| `data_model_documentation_completeness` | Database | Confirm entities and gaps are documented. | Documented entities / expected entities. | Architecture/Engineering | 100% | 100% for current six entities. | Docs | Sprint close | Future builders may invent relationships. |
| `referential_integrity_gap_count` | Database | Track known relationship gaps. | Count documented FK/relationship gaps. | Engineering/Product | Trend down after business decisions | 3 known: User-Driver, OrderState latest refs, missing orders table. | Docs/model review | Per data model sprint | Data integrity assumptions remain implicit. |
| `backend_critical_flow_coverage` | Calidad | Confirm critical backend flows have regression tests. | Covered required flows / required critical backend flows. | Engineering/QA | 100% for Fase 3 list | 100% for health, auth, permissions, events, evidence, OCR, review, AuditLog, config, Alembic. | Pytest/file audit | Sprint close | High-impact backend regressions may ship. |
| `frontend_test_pass_rate` | Calidad | Track frontend component test health. | Passing Vitest tests / total Vitest tests. | Frontend Engineering/QA | 100% | 100%; 8/8 passed in Fase 3. | Vitest | Every frontend change | UI/auth regressions may ship. |
| `auth_test_coverage` | Calidad | Confirm auth behavior is covered. | Auth scenarios covered / required auth scenarios. | Security/Engineering | 100% for Fase 3 list | Covered login success/failure and missing/invalid/current token. | Pytest/Vitest | Every auth change | Broken authentication can ship. |
| `permission_test_coverage` | Calidad | Confirm RBAC behavior is covered. | Permission scenarios covered / required permission scenarios. | Security/Engineering | 100% for Fase 3 list | Covered admin users, supervisor order states/review/OCR, driver restrictions and upload. | Pytest | Every permission change | Broken authorization can ship. |
| `evidence_upload_test_coverage` | Calidad | Confirm evidence validation is covered. | Evidence scenarios covered / required evidence scenarios. | Engineering/QA | 100% for Fase 3 list | Covered valid image, invalid MIME, invalid magic bytes, missing order number. | Pytest | Every upload change | Unsafe or broken uploads can ship. |
| `ocr_review_test_coverage` | Calidad | Confirm OCR/review flow is covered. | OCR/review scenarios covered / required scenarios. | Engineering/QA | 100% for Fase 3 list | Covered mock OCR, result, confirm, pending, detail, human confirm/reject. | Pytest | Every OCR/review change | AI/review regressions can ship. |
| `audit_log_test_coverage` | Calidad | Confirm critical implemented audit actions are covered. | Audited actions tested / critical implemented audit actions. | Security/Engineering | 100% for implemented Fase 3 actions | Covered login success/failure, evidence upload, OCR processed, review confirm/reject; OCR confirm gap documented. | Pytest | Every audit-sensitive change | Forensics gaps can grow silently. |
| `warning_noise_count` | Calidad | Track warnings that can hide real failures. | Count warnings emitted during backend/frontend test runs. | Engineering/QA | Trend down | Backend local: 235 warnings; Docker: 173 warnings; frontend tests: 0 notable warnings. | Test output | Every sprint | Real warning signals may be ignored. |
