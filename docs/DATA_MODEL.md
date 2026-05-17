# Data Model

This document describes entities verified from current SQLAlchemy models. It does not invent relationships or fields that are not implemented.

## Migration Status

Alembic baseline migration exists at:

```text
backend/alembic/versions/20260517_0001_baseline_schema.py
```

The baseline represents the current SQLAlchemy model schema.

Fase 4 adds:

```text
backend/alembic/versions/20260517_0002_add_user_driver_relationship.py
```

This migration adds `users.driver_id`, an index, and a foreign key to `drivers.id`.

## User

Entity: `User`

Purpose: Application user for authentication and role-based authorization.

Primary key: `id`

Important fields:

- `email`
- `full_name`
- `hashed_password`
- `role`
- `driver_id`
- `is_active`
- `created_at`
- `updated_at`

Relationships:

- `audit_logs.user_id` references `users.id`.
- `users.driver_id` references `drivers.id`.

Cardinality:

- A `DRIVER` user must be associated to exactly one active operational `Driver` in application logic.
- `ADMIN` and `SUPERVISOR` may have `driver_id = null`.
- The database does not currently enforce one-to-one uniqueness on `users.driver_id`; this avoids locking future staffing/business rules before assignment policy is finalized.

Indexes / uniqueness:

- `email` is unique and indexed.
- `driver_id` is indexed.

Risks:

- Role is stored as a string without database enum/check constraint.
- Historical users may have `driver_id = null`.
- The role-to-driver requirement is enforced in application logic, not a database check constraint.

Future improvements:

- Add role constraints or enum strategy.
- Decide whether `users.driver_id` should become unique after operational staffing rules are confirmed.

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
- `users.driver_id` references `drivers.id`.

Indexes / uniqueness:

- `phone` is unique.

Risks:

- A user-driver relationship now exists, but route/order assignment beyond driver ownership is not yet formalized.

Future improvements:

- Define order assignment and mobile-first driver workflow.

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

- Historical `DeliveryEvent` and `OrderState` rows may have `driver_id = null`.
- Missing formal `orders` table.
- Missing formal order-to-driver assignment table.
- Missing canonical order status catalog.
- Flexible JSON fields require reporting discipline.
- Evidence retention policy is undefined.
- `OrderState` latest references are not enforced as foreign keys.
