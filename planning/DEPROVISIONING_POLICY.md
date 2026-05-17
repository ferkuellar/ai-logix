# Deprovisioning Policy

## Purpose

Define initial cleanup and removal controls for AI Logix so local, demo, and future cloud resources do not accumulate unmanaged risk.

## Uploads

- Clean orphaned uploads only after confirming no database record references them.
- Do not delete evidence needed for audit, legal, operational, or demo validation.
- Define retention before production.
- Future cleanup jobs must log deleted file count and criteria.

## Demo Users

- Demo users must be clearly identifiable by email or naming convention.
- Demo users should be deactivated, not hard-deleted, unless policy later requires deletion.
- User deactivation must be performed by `ADMIN`.
- User deactivation must be auditable.

## Secrets

- Rotate `SECRET_KEY`, database passwords, seed admin password, and provider API keys before staging or production.
- Do not reuse local `.env` values outside local development.
- Remove unused provider keys immediately.

## Local Containers And Volumes

For a controlled local reset:

```bash
docker compose down
docker compose down -v
```

Use `docker compose down -v` only when intentionally deleting local database state.

## External Resources

No external resources are created in Phase 0.

Before creating external resources, document:

- Owner.
- Purpose.
- Environment.
- Data classification.
- Expected monthly cost if known.
- Review date.
- Deprovisioning procedure.

## Cloud Resource Rule

Cloud resources are prohibited unless they have owner, purpose, environment, data classification, and review date.

## Decision Logging

Every deletion or deprovisioning policy decision that affects production, staging, customer data, or audit records must be recorded in `planning/DECISIONS.md`.
