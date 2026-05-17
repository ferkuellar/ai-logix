# Sprint 000 Blueprint - Foundation Metrics

## Files To Review

- `README.md`
- `docker-compose.yml`
- `.env.example`
- Backend models, routes, dependencies, and config.
- Frontend package scripts.
- Existing docs under `docs/`.
- Existing planning files if present.

## Files To Create

- `AGENTS.md`
- `CODEX.md`
- `CLAUDE.md`
- `.gitignore`
- `planning/STATE.md`
- `planning/DECISIONS.md`
- `planning/DOMAIN.md`
- `planning/RISKS.md`
- `planning/QUESTIONS.md`
- `planning/FILE_INVENTORY.md`
- `planning/METRICS.md`
- `planning/MATURITY_MODEL.md`
- `planning/ADOPTION_MAP.md`
- `planning/TAGGING_STRATEGY.md`
- `planning/AUTOMATION_STRATEGY.md`
- `planning/DEPROVISIONING_POLICY.md`
- `planning/CONTINUOUS_IMPROVEMENT.md`
- `planning/sprints/000-foundation-metrics/requirements.md`
- `planning/sprints/000-foundation-metrics/blueprint.md`
- `planning/sprints/000-foundation-metrics/acceptance.md`
- `planning/sprints/000-foundation-metrics/handoff-prompt.md`
- Phase 0 docs under `docs/`

## Files To Modify

- `.env.example`: sanitize and align with required template.
- Existing Phase 0 docs if already created: improve, do not discard useful context.
- Git index: remove `.env` and Python bytecode artifacts from tracking without deleting local files.

## Step-by-Step Plan

1. Inspect repository structure and existing documentation.
2. Confirm application stack from existing files.
3. Create or update root operating files.
4. Create or update planning memory files.
5. Create or update sprint 000 files.
6. Create or update technical docs.
7. Remove tracked local secrets/generated artifacts from Git index.
8. Validate required files exist.
9. Search for empty files and unresolved placeholders.
10. Run `docker compose config`.
11. Document skipped validations with reason and impact.
12. Update acceptance and final audit.

## Validation

- Required file existence check.
- Empty required file check.
- Placeholder search.
- `.env` ignore/index check.
- `docker compose config`.

Runtime build/tests are optional for Phase 0 because no application code is changed, but the skip must be documented.

## Risks

- `.env` had been tracked before Phase 0 cleanup.
- Python bytecode artifacts had been tracked before Phase 0 cleanup.
- Docker runtime build may still need validation in Phase 1.
- Existing local `.env` values are not inspected to avoid exposing secrets.

## No-Go Items

- No WhatsApp.
- No S3/R2.
- No mobile app.
- No route optimization.
- No autonomous AI agents.
- No application rewrite.
- No business-rule changes.
