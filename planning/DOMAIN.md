# Domain

## Domain Summary

AI Logix operates in the logistics delivery domain. It tracks delivery events, order state, drivers, stores, evidence, OCR/AI extraction, human review, role-based access, and audit records.

No real customer names, client contracts, or private operational assumptions are defined in this repository.

## Orders

An order is represented by `order_number` in delivery events and order state records. The current system stores a latest trusted snapshot in `order_states`.

Open domain issue: official order statuses are not yet formalized.

## Repartidores / Drivers

Drivers are represented by the `drivers` table and may also have application users with role `DRIVER`. The code currently does not enforce a strong one-to-one relationship between `users` and `drivers`.

## Stores

Stores represent delivery destinations or operational locations. The current model includes code, name, address fields, city/state/zone, and optional coordinates.

## Delivery Events

Delivery events record operational changes such as uploaded evidence, status updates, location, observations, OCR text, and AI-extracted JSON.

## Photographic Evidence

Evidence is currently uploaded as JPEG, PNG, or WEBP and stored locally under `backend/uploads`. Evidence upload creates a delivery event and stores metadata in the database.

## OCR / IA

OCR/AI is implemented behind providers. The mock provider supports deterministic local development, and an OpenAI provider is prepared for external processing when configured.

OCR/AI output is advisory until human review.

## Human Review

Human review is the trust boundary. Supervisors/admins confirm or reject AI-extracted data before it is treated as operationally reliable.

## Trusted Operational State

`order_states` stores the latest trusted operational state per order. The current implementation updates order state from delivery events and review workflows. Future work must preserve the human-review trust rule unless a documented decision changes it.

## Audit

`audit_logs` records selected security and operational actions such as login success/failure, evidence upload, OCR processing, review decisions, user creation, and user deactivation.

## Current Roles

- `ADMIN`: manages users and can perform all operational functions.
- `SUPERVISOR`: can view operations, process OCR, and perform human review.
- `DRIVER`: can create delivery events and upload evidence.
