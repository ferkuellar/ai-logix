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
| `backend_test_pass_rate` | Calidad | Track backend correctness. | Passing pytest tests / total pytest tests. | Engineering/QA | 100% | Not run in Phase 0. | Pytest | Every backend change | Regressions can ship. |
| `frontend_build_success` | Calidad | Confirm frontend compiles. | `npm run build` exits 0. | Frontend Engineering | 100% | Not run in Phase 0. | npm/Vite | Every frontend change | Broken UI build. |
| `frontend_lint_success` | Calidad | Confirm frontend lint health. | `npm run lint` exits 0. | Frontend Engineering | 100% | Not run in Phase 0. | npm/ESLint | Every frontend change | Maintainability defects accumulate. |
| `migration_status` | Calidad | Track schema-change safety. | Migration tool present and migrations apply cleanly. | Engineering/DevOps | Formal migrations before production | No formal migrations detected. | Repo/DB | Every schema change | Unsafe schema evolution. |
| `docs_completeness_score` | Calidad | Measure required docs coverage. | Existing required docs / required docs. | Architecture/PM | 100% for Phase 0 | 100% for required Phase 0 docs. | File check | Sprint close | Future builders lack context. |
