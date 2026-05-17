# Data Model

This document describes entities verified from current SQLAlchemy models. It does not invent fields beyond those detected in code.

## User

Purpose: Application user for authentication and role-based authorization.

Main fields:

- `id`
- `email`
- `full_name`
- `hashed_password`
- `role`
- `is_active`
- `created_at`
- `updated_at`

Known relationships:

- `audit_logs.user_id` can reference `users.id`.

Missing relationships:

- No verified strong one-to-one relationship between `users` with role `DRIVER` and `drivers`.

Risks:

- Driver users may not be strongly tied to driver operational records.
- Role is a string and should be constrained before production.

## Driver

Purpose: Operational driver profile.

Main fields:

- `id`
- `name`
- `phone`
- `email`
- `vehicle`
- `status`
- `created_at`

Known relationships:

- `delivery_events.driver_id` references `drivers.id`.

Missing relationships:

- No verified foreign key from `users` to `drivers`.

Risks:

- Assignment and identity model need business definition.

## Store

Purpose: Store or delivery destination record.

Main fields:

- `id`
- `store_code`
- `store_name`
- `address`
- `city`
- `state`
- `latitude`
- `longitude`
- `zone`
- `created_at`

Known relationships:

- `delivery_events.store_id` references `stores.id`.

Missing relationships:

- No verified route, customer, or account model.

Risks:

- Store data quality affects maps and reporting.

## DeliveryEvent

Purpose: Operational event, evidence record, OCR record, and review-related data container.

Main fields:

- `id`
- `event_type`
- `order_number`
- `driver_id`
- `store_id`
- `status`
- `latitude`
- `longitude`
- `photo_url`
- `ocr_text`
- `ai_extracted_json`
- `observations`
- `payload_json`
- `created_at`

Known relationships:

- Optional `driver_id` foreign key to `drivers.id`.
- Optional `store_id` foreign key to `stores.id`.

Missing relationships:

- No verified order table exists; `order_number` is a string.
- Review state appears represented in JSON/service behavior, not a dedicated table.

Risks:

- JSON fields can complicate reporting.
- Status strings need canonical values.

## OrderState

Purpose: Latest trusted operational state for an order.

Main fields:

- `id`
- `order_number`
- `current_status`
- `store_id`
- `driver_id`
- `last_event_id`
- `last_latitude`
- `last_longitude`
- `last_update_at`

Known relationships:

- `order_number` is unique.

Missing relationships:

- `store_id`, `driver_id`, and `last_event_id` are UUID fields but not verified as explicit foreign keys in the model.

Risks:

- Referential integrity may not be enforced for latest-state references.
- Current status values are not constrained.

## AuditLog

Purpose: Minimal security and operational audit trail.

Main fields:

- `id`
- `user_id`
- `action`
- `resource_type`
- `resource_id`
- `metadata_json`
- `ip_address`
- `created_at`

Known relationships:

- Optional `user_id` foreign key to `users.id`.

Missing relationships:

- No dedicated audit retention policy.

Risks:

- Critical action coverage is partial.
- Audit detail may be insufficient for production compliance.
