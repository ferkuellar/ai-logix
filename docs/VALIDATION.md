# Validation

## Validation Matrix

| Area | Command or Method | Expected Result | Status | Notes |
| --- | --- | --- | --- | --- |
| Documentation files | Required file existence check | All required files exist. | Passed | Verified in final review. |
| Empty required files | File length check | No required file is empty. | Passed | Verified in final review. |
| Placeholder cleanup | Search for unresolved placeholders in Phase 0 files | No unresolved placeholder. | Passed | Open uncertainties are in `planning/QUESTIONS.md`. |
| Docker Compose config | `docker compose config` | Exit code 0 and rendered config. | Passed | Executed successfully. |
| Backend health | `GET http://localhost:8000/api/health` | JSON status ok. | Not executed | Requires running services. No app code changed in Phase 0. |
| Auth | Login with seeded admin. | JWT returned. | Not executed | Requires running services and seed. Covered by existing tests but not run in Phase 0. |
| Permissions | Exercise ADMIN/SUPERVISOR/DRIVER routes. | Forbidden/allowed behavior matches matrix. | Not executed | No auth code changed. Existing backend tests cover permissions. |
| Upload | Upload valid and invalid images. | Valid accepted; invalid rejected. | Not executed | No upload code changed. Existing backend tests cover evidence upload. |
| OCR mock | Process evidence with `OCR_PROVIDER=mock`. | OCR result generated. | Not executed | No OCR code changed. Existing backend tests cover OCR flow. |
| Human review | Confirm/reject review item. | Review status updated and audit logged. | Not executed | No review code changed. Existing backend tests cover review. |
| Audit | Inspect `audit_logs`. | Critical actions recorded. | Not executed | Requires running DB. Audit model/routes documented. |
| Frontend build | `cd frontend && npm run build` | Exit code 0. | Not executed | No frontend code changed. |
| Frontend lint | `cd frontend && npm run lint` | Exit code 0. | Not executed | No frontend code changed. |
| Metrics | Compare `planning/METRICS.md` and `docs/METRICS.md`. | Required categories and metrics defined. | Passed | Metrics definitions complete; instrumentation gaps documented. |

## Executed Commands

```bash
docker compose config
```

Result: passed.

## Commands Not Executed

### `docker compose up --build`

Result: not executed.

Cause: Phase 0 changed documentation, `.gitignore`, `.env.example`, and Git index hygiene only. It did not change application code or Docker files.

Impact: Runtime startup is not revalidated in this pass. Risk is acceptable for Phase 0 and should be closed in Phase 1 or before demo.

Next action: run before any demo or code-bearing sprint closure.

### `docker compose exec backend pytest`

Result: not executed.

Cause: Backend services were not started and no backend application code changed.

Impact: Existing tests were not refreshed in this phase. Risk is low for documentation-only changes and should be included in Phase 1 CI.

Next action: run after `docker compose up --build` or in future CI.

### `cd frontend && npm install && npm run build && npm run lint`

Result: not executed.

Cause: No frontend source or dependency file changed in Phase 0. Running `npm install` could modify local dependency artifacts.

Impact: Frontend build/lint health is not refreshed by this phase. Risk is low for documentation-only changes and should be included in Phase 1 CI.

Next action: run in Phase 1 CI setup or before demo.
