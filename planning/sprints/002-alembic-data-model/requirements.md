# Sprint 002 Requirements - Alembic Data Model

## Problema

AI Logix used SQLAlchemy model metadata for local schema creation but did not have formal migrations. This is unsafe for serious schema evolution.

## Objetivo

Add Alembic migration flow, create a baseline migration for the current schema, document migration operations, and stabilize data model documentation.

## Usuarios afectados

- Backend Engineering: needs controlled schema evolution.
- DevOps: needs migration commands and rollback policy.
- QA: needs validation for migration files.
- Future builders: need baseline and data model context.

## Alcance

- Add Alembic dependency and configuration.
- Create baseline migration for current models.
- Configure Alembic to use runtime settings.
- Restrict `Base.metadata.create_all` to development.
- Add structural Alembic tests.
- Update database migration and data model docs.
- Update planning, risks, metrics, validation, and audit.

## Fuera de alcance

- Model redesign.
- `User` to `Driver` relationship implementation.
- Rate limiting.
- S3/R2.
- `/uploads` protection.
- WhatsApp.
- Mobile app.
- CI/CD.
- Business rule changes.
- Data deletion.
- Cloud resources.

## Reglas tecnicas

- Migration baseline must reflect current SQLAlchemy models.
- Do not drop existing tables.
- Do not invent tables or relationships.
- Use `settings.database_url`; do not hardcode secrets.
- Review migrations manually before applying.
- Do not edit migrations already applied to shared environments.

## Riesgos

- Existing databases created by `create_all` may need Alembic stamping before future upgrades.
- Downgrades can become limited when future migrations alter data.
- CI/CD does not yet enforce migration checks.
- Backup/restore is still required before production migrations.

## Metricas

- `migration_status`
- `migration_head_current`
- `schema_baseline_created`
- `alembic_history_available`
- `create_all_restricted`
- `data_model_documentation_completeness`
- `referential_integrity_gap_count`

## Criterios de aceptacion

Acceptance is tracked in `acceptance.md`.
