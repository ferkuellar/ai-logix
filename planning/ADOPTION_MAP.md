# Adoption Map

## Stage 1 - Internal technical stabilization

Objective: Stabilize repository, documentation, security baseline, validation commands, and local workflow.

Users involved: Engineering, DevOps, technical lead.

Entry metrics:

- `docs_completeness_score`
- `docker_compose_valid`
- `secrets_in_repo_count`

Exit metrics:

- Required docs complete.
- `docker compose config` passes.
- `.env` is not tracked.

Risks:

- Missing CI/CD.
- Defaults copied into later environments.

Advance criterion: Phase 0 acceptance is complete and Phase 1 security scope is approved.

## Stage 2 - Supervisor dashboard validation

Objective: Confirm supervisors can use dashboard/review views for operational visibility.

Users involved: Supervisors, product owner, frontend/backend engineering.

Entry metrics:

- `order_state_coverage`
- `human_review_pending_count`
- `api_health_status`

Exit metrics:

- Supervisor can view order states.
- Review queue metrics are understandable.
- Permission checks are confirmed.

Risks:

- Order statuses are not canonical.
- Review SLA is undefined.

Advance criterion: Supervisor workflow is validated with agreed order statuses.

## Stage 3 - Driver workflow validation

Objective: Confirm drivers can create delivery events and upload evidence.

Users involved: Drivers, supervisors, product owner.

Entry metrics:

- `upload_success_rate`
- `upload_rejection_rate`
- `protected_endpoint_coverage`

Exit metrics:

- Driver evidence workflow succeeds with valid images.
- Invalid files are rejected clearly.
- Driver does not access global dashboard.

Risks:

- User-driver relationship is not strongly enforced.
- Evidence requirements by delivery type are undefined.

Advance criterion: Driver workflow and assignment rules are documented.

## Stage 4 - OCR/human review operational pilot

Objective: Validate OCR provider strategy and human review trust boundary.

Users involved: Supervisors, operations, engineering.

Entry metrics:

- `ocr_processed_count`
- `ocr_human_review_required_rate`
- `human_review_pending_count`

Exit metrics:

- OCR mock flow works.
- Review confirm/reject flow works.
- Review SLA target is defined.

Risks:

- OCR can fail or return low confidence.
- Rejected OCR handling is not fully defined.

Advance criterion: OCR failure and low-confidence rules are approved.

## Stage 5 - Client/demo readiness

Objective: Prepare a reliable demo using local or controlled dev environment.

Users involved: Product, sales/demo owner, engineering.

Entry metrics:

- `api_health_status`
- `frontend_build_success`
- `backend_test_pass_rate`

Exit metrics:

- Demo checklist passes.
- Seed data and demo users are controlled.
- No real secrets or private evidence are used.

Risks:

- Demo data can be mistaken for production data.
- Runtime build may fail if not validated.

Advance criterion: Demo dry run passes end to end.

## Stage 6 - Production hardening

Objective: Prepare for real operational usage.

Users involved: Engineering, DevOps, Security, Product/Ops.

Entry metrics:

- `secrets_in_repo_count`
- `migration_status`
- `api_error_rate`
- `audit_log_critical_action_coverage`

Exit metrics:

- Secrets are managed.
- Migrations exist.
- Backup/restore is defined.
- Upload access and retention are approved.
- CI/CD gates are active.

Risks:

- Local evidence storage is insufficient.
- Lack of observability can hide incidents.

Advance criterion: Security, deployment, backup, and observability controls are approved.
