# Permissions

## Role Summary

- `ADMIN`: user management and all operational capabilities.
- `SUPERVISOR`: operational visibility, OCR processing, and human review.
- `DRIVER`: delivery event creation and evidence upload.

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
| `POST /api/delivery-events` | Yes | Yes | Yes |
| `POST /api/evidence/upload` | Yes | Yes | Yes |
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
- `DRIVER` can create events and upload evidence.
- OCR and review are administrative/supervisory functions.
- The current code does not verify a strong `User` to `Driver` domain relationship.
- Frontend route protection is UX only; backend role checks are authoritative.

## Risk Link

The missing strong user-driver relationship is tracked in `planning/RISKS.md` and `planning/QUESTIONS.md`.
