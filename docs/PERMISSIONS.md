# Permissions

## Role Summary

- `ADMIN`: user management and all operational capabilities.
- `SUPERVISOR`: operational visibility, OCR processing, and human review.
- `DRIVER`: delivery event creation and evidence upload only for their assigned `driver_id`.

## Matrix

| Endpoint / Area | ADMIN | SUPERVISOR | DRIVER |
| --- | --- | --- | --- |
| `POST /api/auth/login` | Yes | Yes | Yes |
| `GET /api/auth/me` | Yes | Yes | Yes |
| `GET /api/users` | Yes | No | No |
| `POST /api/users` | Yes | No | No |
| `GET /api/users/{user_id}` | Yes | Own user only | Own user only |
| `PATCH /api/users/{user_id}` | Yes | No | No |
| `DELETE /api/users/{user_id}` | Yes | No | No |
| `GET /api/order-states` | Yes | Yes | No |
| `POST /api/delivery-events` | Any valid driver | Any valid driver | Own assigned `driver_id` only |
| `POST /api/evidence/upload` | Any valid driver or no driver | Any valid driver or no driver | Own assigned `driver_id` only |
| `POST /api/ocr/process/{event_id}` | Yes | Yes | No |
| `GET /api/ocr/result/{event_id}` | Yes | Yes | No |
| `POST /api/ocr/confirm/{event_id}` | Yes | Yes | No |
| `GET /api/review/pending` | Yes | Yes | No |
| `GET /api/review/{event_id}` | Yes | Yes | No |
| `POST /api/review/{event_id}/confirm` | Yes | Yes | No |
| `POST /api/review/{event_id}/reject` | Yes | Yes | No |
| Global dashboard/order state visibility | Yes | Yes | No |
| OCR/review administration | Yes | Yes | No |

## Limitations

- `DRIVER` must not access global dashboard/order-state views.
- `DRIVER` can create events and upload evidence only when associated to a `Driver`.
- `DRIVER` without `driver_id` receives `403` for operational actions.
- `DRIVER` cannot operate with another driver's `driver_id`; cross-driver attempts receive `403`.
- If `DRIVER` omits `driver_id`, the backend assigns the authenticated user's own `driver_id`.
- `ADMIN` and `SUPERVISOR` retain global operational visibility and may operate for any valid `driver_id`.
- OCR and review are administrative/supervisory functions.
- Frontend route protection is UX only; backend role checks are authoritative.
- Fase 4 enforces ownership by `driver_id`, not yet by route, order assignment, or delivery manifest.

## Risk Link

Residual driver workflow risks are tracked in `planning/RISKS.md` and `planning/QUESTIONS.md`.
