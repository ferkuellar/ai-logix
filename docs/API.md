# API

Local base URL:

```text
http://localhost:8000/api
```

Authentication: bearer JWT unless endpoint is marked public.

## Endpoints

| Method | Path | Purpose | Required Role | Request / Response Known | Documentation Status |
| --- | --- | --- | --- | --- | --- |
| GET | `/api/health` | Health check. | Public | Returns status/service JSON. | Verified from route. |
| POST | `/api/auth/login` | Authenticate user and return JWT. | Public | Request: email/password schema. Response: access token and token type. | Verified from route/schema names. |
| GET | `/api/auth/me` | Read current authenticated user. | Any authenticated active user | Response: current user schema. | Verified. |
| GET | `/api/users` | List users. | `ADMIN` | Response: list of users. | Verified. |
| POST | `/api/users` | Create user. | `ADMIN` | Request: user create schema. Response: user. | Verified. |
| GET | `/api/users/{user_id}` | Read user by ID. | `ADMIN` or same user | Response: user. | Verified. |
| PATCH | `/api/users/{user_id}` | Update user. | `ADMIN` | Request: partial user update. Response: user. | Verified. |
| DELETE | `/api/users/{user_id}` | Deactivate user. | `ADMIN` | Response: deactivated user. | Verified. |
| GET | `/api/order-states` | List latest order states. | `ADMIN`, `SUPERVISOR` | Response: list of order state records. | Verified. |
| POST | `/api/delivery-events` | Create delivery event and update order state when possible. | `ADMIN`, `SUPERVISOR`, `DRIVER` | Request: delivery event create schema. Response: delivery event. | Verified. |
| POST | `/api/evidence/upload` | Upload photo evidence and create event. | `ADMIN`, `SUPERVISOR`, `DRIVER` | Multipart form with order/status/location/observations/file. Response: event ID, photo URL, metadata. | Verified. |
| POST | `/api/ocr/process/{event_id}` | Run OCR provider for event evidence. | `ADMIN`, `SUPERVISOR` | Response: event ID, OCR text, extracted JSON. | Verified. |
| GET | `/api/ocr/result/{event_id}` | Read OCR result. | `ADMIN`, `SUPERVISOR` | Response: event/OCR details. | Verified. |
| POST | `/api/ocr/confirm/{event_id}` | Confirm OCR result through legacy endpoint. | `ADMIN`, `SUPERVISOR` | Request: OCR confirm schema. Response: confirmed result. | Verified; human review endpoints are preferred. |
| GET | `/api/review/pending` | List pending human review items. | `ADMIN`, `SUPERVISOR` | Query supports status/order/limit/offset. Response: list. | Verified. |
| GET | `/api/review/{event_id}` | Read review detail. | `ADMIN`, `SUPERVISOR` | Response: review detail. | Verified. |
| POST | `/api/review/{event_id}/confirm` | Confirm human review. | `ADMIN`, `SUPERVISOR` | Request: confirm schema. Response: review result. | Verified. |
| POST | `/api/review/{event_id}/reject` | Reject human review. | `ADMIN`, `SUPERVISOR` | Request: reject schema. Response: review result. | Verified. |

## Notes

- The API currently returns FastAPI/Pydantic responses directly.
- Standard envelope responses are not currently enforced.
- Error response standardization can be considered in a future API hardening sprint.
- Auth and permission behavior is documented in `docs/PERMISSIONS.md`.
