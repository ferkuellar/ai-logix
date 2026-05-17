# Sprint 004 Handoff Prompt

Read `AGENTS.md` first.

Then read:

1. `planning/STATE.md`
2. `planning/DECISIONS.md`
3. `planning/DOMAIN.md`
4. `planning/RISKS.md`
5. `planning/METRICS.md`
6. `planning/sprints/004-driver-permissions/`
7. `docs/PERMISSIONS.md`
8. `docs/API.md`
9. `docs/DATA_MODEL.md`

Rules:

- Do not implement features outside DRIVER ownership/asignacion.
- DRIVER cannot operate resources for another `driver_id`.
- DRIVER without `driver_id` cannot perform operational actions.
- ADMIN/SUPERVISOR keep global operational scope.
- Validate against `acceptance.md`.
- Update docs, risks, metrics, and audit.

Suggested commit:

```text
security: enforce driver ownership and operational assignment
```
