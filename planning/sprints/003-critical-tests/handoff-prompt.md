# Sprint 003 Handoff Prompt

You are working on AI Logix. Read `AGENTS.md` first.

Then read:

1. `planning/STATE.md`
2. `planning/DECISIONS.md`
3. `planning/DOMAIN.md`
4. `planning/RISKS.md`
5. `planning/METRICS.md`
6. `planning/sprints/003-critical-tests/`
7. `docs/TESTING.md`
8. `docs/VALIDATION.md`

Rules:

- Do not implement features outside critical tests.
- Do not weaken security or permissions to make tests pass.
- Do not use OpenAI real in tests; use mock OCR provider.
- Do not depend on external services.
- Validate against `acceptance.md`.
- Update documentation, risks, metrics, and state when behavior changes.
- Report files changed, tests run, failures, residual risks, and suggested commit.

Suggested commit:

```text
test: add critical backend and frontend regression coverage
```
