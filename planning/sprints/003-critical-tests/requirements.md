# Sprint 003 Requirements - Critical Tests

## Problema

AI Logix ya tiene flujos backend y frontend funcionales, pero necesita una suite de regresion critica que haga visibles las roturas en auth, permisos, evidencia, OCR, revision humana, migraciones y shell frontend antes de continuar con features operativas.

## Objetivo

Consolidar una suite backend/frontend repetible que cubra los flujos criticos actuales sin cambiar reglas de negocio ni depender de servicios externos.

## Usuarios afectados

- Engineering: necesita confianza para cambiar backend/frontend.
- QA: necesita comandos reproducibles para validar entregas.
- Supervisores: dependen de dashboard, revision y order states.
- Drivers: dependen de carga de evidencia y eventos.
- Seguridad/DevOps: necesita pruebas sobre auth, config y permisos.

## Alcance

- Auditar tests existentes.
- Agregar cobertura backend faltante para health, auth, permisos, delivery events, evidencia, OCR, human review, AuditLog, config y Alembic.
- Agregar Vitest + Testing Library para frontend.
- Agregar tests frontend minimos de render, login, auth/localStorage y dashboard con API mockeada.
- Limpiar uploads temporales durante tests.
- Documentar comandos y resultados.

## Fuera de alcance

- No implementar permisos DRIVER reales nuevos.
- No cambiar modelo de datos.
- No implementar CI/CD.
- No agregar E2E pesado.
- No buscar cobertura perfecta.
- No depender de OpenAI ni servicios externos.

## Flujos criticos

- Healthcheck backend.
- Login exitoso/fallido.
- Token ausente/invalido.
- RBAC basico ADMIN/SUPERVISOR/DRIVER.
- Creacion de delivery events y actualizacion de order states.
- Upload valido y rechazos de evidencia.
- OCR mock process/result/confirm.
- Human review pending/detail/confirm/reject.
- AuditLog para acciones criticas implementadas.
- Configuracion segura y Alembic baseline.
- Frontend login, sesion localStorage, dashboard y API mock.

## Metricas

- `backend_test_pass_rate`
- `backend_critical_flow_coverage`
- `frontend_test_pass_rate`
- `frontend_build_success`
- `frontend_lint_success`
- `auth_test_coverage`
- `permission_test_coverage`
- `evidence_upload_test_coverage`
- `ocr_review_test_coverage`
- `audit_log_test_coverage`
- `warning_noise_count`

## Riesgos

- La suite backend usa SQLite in-memory para rapidez; no reemplaza pruebas PostgreSQL completas.
- Warnings de Pydantic y `datetime.utcnow` siguen presentes.
- Tests frontend mockean Leaflet y API, no validan browser real.
- CI/CD aun no ejecuta la suite automaticamente.

## Entregables

- Backend tests criticos agregados.
- Frontend test runner y tests minimos.
- `docs/TESTING.md`.
- Actualizaciones de `docs/VALIDATION.md`, `docs/OPERATIONS.md`, `docs/METRICS.md`.
- Actualizaciones de planning.
- Auditoria final de Fase 3.

## Criterios de aceptacion

Los criterios verificables estan en `planning/sprints/003-critical-tests/acceptance.md`.
