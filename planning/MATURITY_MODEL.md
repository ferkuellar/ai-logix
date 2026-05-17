# Maturity Model

## Level 0 - Chat-driven prototype

Characteristics:

- Main project memory lives in conversation.
- Scope can drift between sessions.
- Documentation is incomplete or missing.
- Validation is ad hoc.

AI Logix status: surpassed.

## Level 1 - Documented repo

Characteristics:

- Canonical `AGENTS.md`.
- Durable `planning/` memory.
- Architecture, API, data model, permissions, operations, validation, and metrics docs exist.
- Risks, decisions, and questions are visible.
- Required sprint 000 files exist.

AI Logix status: complete for Phase 0.

## Level 2 - Sprint-based delivery

Characteristics:

- Every sprint has requirements, blueprint, acceptance, and handoff prompt.
- Scope is approved before implementation.
- Acceptance is checked before closure.
- Durable decisions and risks are updated per sprint.

AI Logix status: preparing Level 2.

## Level 3 - Validated workflows

Characteristics:

- Backend tests run reliably.
- Frontend build/lint run reliably.
- Auth, permissions, upload, OCR mock, review, and audit smoke tests are documented and repeated.
- Migrations are validated.

AI Logix status: not complete; requires CI and migration strategy.

## Level 4 - Observable operations

Characteristics:

- Logs, metrics, alerts, and dashboards exist.
- API health, error rate, latency, review SLA, upload rates, OCR quality, and audit coverage are measured.
- Demo/production readiness is based on measured signals.

AI Logix status: metrics are defined but not fully instrumented.

## Level 5 - Controlled automation

Characteristics:

- CI/CD gates enforce validation.
- Secret scanning prevents leaks.
- Deployment is environment-aware.
- Deprovisioning and retention are automated or formally controlled.

AI Logix status: future target.

## Current Target

Current target: Level 1 complete, preparing Level 2.

What remains for Level 2:

- Select the next sprint.
- Use the sprint folder as the handoff.
- Validate changes against acceptance on every sprint.
