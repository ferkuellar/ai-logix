# Metrics

Metrics are defined in detail in `planning/METRICS.md`. This document explains how to interpret them operationally.

## Categories

### Producto

Measures whether the product supports real logistics workflows:

- Order state coverage.
- Evidence capture.
- Pending reviews.
- Review SLA.
- Orders without current status.

### Operacion

Measures system operability:

- API health.
- Backend startup.
- Docker Compose validity.
- Upload success/rejection.
- API error rate.

### Seguridad

Measures access and security posture:

- Secrets in repo.
- Protected endpoint coverage.
- Failed logins.
- Audit coverage.
- Default secret detection.
- Environment template completeness.
- Unsafe production config blocking.
- Wildcard CORS blocking.
- Security config test health.
- Driver ownership enforcement.
- Driver cross-access denials.

### OCR / IA

Measures OCR/AI usefulness and risk:

- OCR processed.
- OCR failed.
- Confidence average.
- Human review required rate.
- Confirmed/rejected OCR rates.

### Calidad

Measures engineering health:

- Backend tests.
- Backend critical flow coverage.
- Frontend tests.
- Frontend build.
- Frontend lint.
- Migration status.
- Documentation completeness.
- Warning noise.

### Database

Measures schema governance:

- Alembic baseline exists.
- Migration history is readable.
- Database revision is at migration head.
- Automatic `create_all` is restricted outside development.
- Data model documentation covers current entities and known gaps.

## Red / Yellow / Green Interpretation

| Color | Meaning | Action |
| --- | --- | --- |
| Green | Metric meets target or current phase expectation. | Continue monitoring. |
| Yellow | Metric is partially measured, target missing, or needs review. | Assign owner and close gap in upcoming sprint. |
| Red | Metric fails target, is unmeasured for production-critical area, or indicates security risk. | Prioritize immediately. |

## Minimum Metrics For Demo

- `docker_compose_valid`
- `api_health_status`
- `backend_startup_success`
- `frontend_build_success`
- `frontend_lint_success`
- `frontend_test_pass_rate`
- `backend_critical_flow_coverage`
- `auth_test_coverage`
- `permission_test_coverage`
- `permission_regression_test_pass_rate`
- `driver_user_assignment_coverage`
- `driver_ownership_enforcement`
- `driver_forbidden_cross_access_count`
- `driver_operational_action_success_rate`
- `driver_unassigned_user_count`
- `evidence_upload_test_coverage`
- `ocr_review_test_coverage`
- `audit_log_test_coverage`
- `warning_noise_count`
- `secrets_in_repo_count`
- `upload_success_rate`
- `ocr_processed_count`
- `human_review_pending_count`

## Minimum Metrics For Production

- All demo metrics.
- `api_error_rate`
- `failed_login_count`
- `protected_endpoint_coverage`
- `audit_log_critical_action_coverage`
- `default_secret_detected`
- `env_example_completeness`
- `unsafe_production_config_blocked`
- `cors_wildcard_blocked`
- `config_security_tests_passed`
- `migration_status`
- `migration_head_current`
- `schema_baseline_created`
- `alembic_history_available`
- `create_all_restricted`
- `data_model_documentation_completeness`
- `referential_integrity_gap_count`
- `human_review_sla_minutes`
- `ocr_failed_count`
- Evidence retention/storage usage metric.

## Frequency

- Development: per sprint or per meaningful change.
- Demo: before every demo.
- Production: daily for operational/security signals, weekly for product/OCR quality, per release for quality gates.

## Recommended Owners

- Product/Ops: product and review metrics.
- Engineering: API, upload, OCR, quality metrics.
- Security/DevOps: secrets, auth, audit, deployment metrics.
- Supervisors: review queue and SLA operational metrics.
