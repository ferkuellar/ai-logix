# Sprint 000 Requirements - Foundation Metrics

## Problem

AI Logix already has functional backend, frontend, database, Docker Compose, evidence upload, OCR, human review, JWT, roles, and minimal audit. The repository needs a durable operating system so future work is guided by files, not conversation memory.

## Objective

Complete the Axon-AI Foundation Metrics operating system without adding product features or changing business rules.

## Users

- Engineering: needs architecture, validation, risks, and handoff clarity.
- DevOps: needs local runtime, automation plan, secrets policy, and future CI/CD direction.
- Product/Ops: needs domain questions, metrics, adoption path, and risk visibility.
- Future builders: need canonical instructions and sprint handoff.

## Scope

- Canonical `AGENTS.md`.
- Thin adapters `CODEX.md` and `CLAUDE.md`.
- `.gitignore` and `.env.example` hygiene.
- Planning memory under `planning/`.
- Sprint 000 handoff files.
- Technical docs under `docs/`.
- Metrics registry.
- Phase 0 audit and acceptance closure.

## Out Of Scope

- New project creation.
- Nested repo creation.
- Backend/frontend rewrite.
- WhatsApp.
- S3/R2.
- Mobile app.
- Route optimization.
- Autonomous AI agents.
- Business rule changes.
- Application code changes.

## Rules

- Preserve existing backend, frontend, docs, and Docker Compose.
- Read files before modifying them.
- No required file may be empty.
- No unresolved placeholder may remain.
- If validation cannot run, document reason, impact, and next action.
- Only mark acceptance criteria complete when true.

## Metrics

Sprint success is measured by:

- `docs_completeness_score`
- `docker_compose_valid`
- `secrets_in_repo_count`
- `migration_status`
- `protected_endpoint_coverage`

Detailed metric definitions live in `planning/METRICS.md`.

## Risks

Primary risks are tracked in `planning/RISKS.md`, including migrations, secrets, upload exposure, rate limiting, OCR quality, evidence retention, dependency pinning, CI/CD, order status taxonomy, and review SLA.

## Open Questions

Open business and operational questions are tracked in `planning/QUESTIONS.md`. Phase 0 does not answer missing business rules.

## Deliverables

- Root operating files.
- Planning files.
- Sprint files.
- Docs files.
- Final audit.
- Completed acceptance.
- Concrete Fase 1 recommendation.
