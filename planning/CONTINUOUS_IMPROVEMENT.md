# Continuous Improvement

## Cycle

1. Measure.
2. Detect gaps.
3. Prioritize by severity.
4. Create sprint.
5. Implement.
6. Validate.
7. Document decision.
8. Update metrics.

## Cadence

| Cadence | Purpose | Output |
| --- | --- | --- |
| Daily during development | Catch blockers, validation failures, and scope drift. | Updated notes in sprint files when needed. |
| Weekly technical review | Review risks, metrics, test health, and open questions. | Updated `RISKS.md`, `METRICS.md`, `QUESTIONS.md`. |
| Per phase audit | Confirm acceptance and operating-system completeness. | Updated phase audit doc. |
| Before demo | Confirm demo workflow, seed data, secrets, and UI/API health. | Demo checklist in docs or sprint acceptance. |
| Before production | Confirm security, migrations, backups, observability, and retention. | Production readiness audit. |

## Prioritization

Prioritize in this order:

1. Security and data exposure.
2. Broken core workflows.
3. Validation gaps.
4. Observability gaps.
5. Documentation gaps.
6. UX and workflow improvements.

## Required Updates At Sprint Close

- `planning/STATE.md`
- `planning/DECISIONS.md`
- `planning/RISKS.md`
- `planning/QUESTIONS.md`
- `planning/METRICS.md`
- Active sprint `acceptance.md`
- Relevant docs in `docs/`
