# Data Model

This document describes entities verified from current SQLAlchemy models. It does not invent relationships or fields that are not implemented.

## Migration Status

Alembic baseline migration exists at:

```text
backend/alembic/versions/20260517_0001_baseline_schema.py
```

The baseline represents the current SQLAlchemy model schema.

## User

Entity: `User`

Purpose: Application user for authentication and role-based authorization.

Primary key: `id`

Important fields:

- `email`
- `full_name`
- `hashed_password`
- `role`
- `is_active`
- `created_at`
- `updated_at`

Relationships:

- `audit_logs.user_id` references `users.id`.

Indexes / uniqueness:

- `email` is unique and indexed.

Risks:

- Role is stored as a string without database enum/check constraint.
- No formal relationship exists between `users` and `drivers`.

Future improvements:

- Evaluate `User` to `Driver` relationship.
- Add role constraints or enum strategy.

## Driver

Entity: `Driver`

Purpose: Operational driver profile.

Primary key: `id`

Important fields:

- `name`
- `phone`
- `email`
- `vehicle`
- `status`
- `created_at`

Relationships:

- `delivery_events.driver_id` references `drivers.id`.

Indexes / uniqueness:

- `phone` is unique.

Risks:

- No enforced link from `users.role = DRIVER` to `drivers`.
- Driver assignment rules are not formalized.

Future improvements:

- Define identity and assignment model for drivers.

## Store

Entity: `Store`

Purpose: Store or delivery destination record.

Primary key: `id`

Important fields:

- `store_code`
- `store_name`
- `address`
- `city`
- `state`
- `latitude`
- `longitude`
- `zone`
- `created_at`

Relationships:

- `delivery_events.store_id` references `stores.id`.

Indexes / uniqueness:

- `store_code` is unique.

Risks:

- No formal customer/account relationship exists.
- Store data quality affects map and reporting accuracy.

Future improvements:

- Add import/validation process for store master data.

## DeliveryEvent

Entity: `DeliveryEvent`

Purpose: Operational event, evidence record, OCR result container, and review-related JSON holder.

Primary key: `id`

Important fields:

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

Relationships:

- `driver_id` references `drivers.id`.
- `store_id` references `stores.id`.

Indexes / uniqueness:

- No model-defined index detected for `order_number`.

Risks:

- `order_number` is a string without a formal `orders` table.
- JSON fields support flexible iteration but can weaken validation/reporting.
- Status values are not constrained by catalog.

Future improvements:

- Define official order/status model.
- Add indexes after query patterns are confirmed.
- Consider typed review/OCR state tables if reporting grows.

## OrderState

Entity: `OrderState`

Purpose: Latest trusted operational state for an order.

Primary key: `id`

Important fields:

- `order_number`
- `current_status`
- `store_id`
- `driver_id`
- `last_event_id`
- `last_latitude`
- `last_longitude`
- `last_update_at`

Relationships:

- No explicit foreign keys are defined for `store_id`, `driver_id`, or `last_event_id`.
- `order_number` links conceptually to delivery events by string value.

Indexes / uniqueness:

- `order_number` is unique.

Risks:

- Referential integrity is not enforced for latest-state references.
- Missing order status catalog can cause inconsistent reporting.

Future improvements:

- Evaluate explicit foreign keys after business rules are confirmed.
- Add canonical order status taxonomy.

## AuditLog

Entity: `AuditLog`

Purpose: Minimal security and operational audit trail.

Primary key: `id`

Important fields:

- `user_id`
- `action`
- `resource_type`
- `resource_id`
- `metadata_json`
- `ip_address`
- `created_at`

Relationships:

- `user_id` references `users.id`.

Indexes / uniqueness:

- No model-defined index detected.

Risks:

- Audit coverage is minimal.
- Retention policy is not defined.
- JSON metadata can vary by action.

Future improvements:

- Define critical action coverage.
- Add retention policy.
- Add indexes for audit reporting if needed.

## Known Data Model Gaps

- Missing formal `User` to `Driver` relationship.
- Missing formal `orders` table.
- Missing canonical order status catalog.
- Flexible JSON fields require reporting discipline.
- Evidence retention policy is undefined.
- `OrderState` latest references are not enforced as foreign keys.
