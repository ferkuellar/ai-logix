# Sprint 004 Requirements - Driver Permissions

## Problema

AI Logix tenia permisos por rol para `DRIVER`, pero no una relacion formal entre usuario autenticado y repartidor operativo. Eso permitia que un DRIVER pudiera crear eventos o subir evidencia con `driver_id` ajeno o sin identidad operacional verificable.

## Objetivo

Implementar ownership real por `driver_id`: un usuario `DRIVER` debe estar asociado a un `Driver` y solo puede operar sobre su propio `driver_id`.

## Usuarios afectados

- Drivers: quedan limitados a su identidad operativa.
- Supervisores: mantienen operacion global.
- Administradores: pueden crear/asignar usuarios DRIVER.
- Seguridad/Ops: obtiene reglas auditables de ownership.

## Alcance

- Agregar `users.driver_id`.
- Crear migracion Alembic.
- Validar creacion/actualizacion de usuarios DRIVER.
- Enforce ownership en delivery events y evidence upload.
- Mantener permisos ADMIN/SUPERVISOR.
- Agregar tests backend y frontend de regresion.
- Actualizar docs y planning.

## Fuera de alcance

- No app movil.
- No S3/R2.
- No proteger `/uploads`.
- No CI/CD.
- No rate limit.
- No tabla formal de asignacion orden-driver.
- No optimizacion de rutas.

## Reglas de negocio

- Un usuario `DRIVER` debe tener exactamente un `driver_id` para operar.
- `ADMIN` y `SUPERVISOR` pueden tener `driver_id = null`.
- `ADMIN` y `SUPERVISOR` pueden operar para cualquier `driver_id` valido.
- `DRIVER` no puede operar otro `driver_id`.
- Si `DRIVER` omite `driver_id`, se usa su `current_user.driver_id`.
- `DRIVER` sin `driver_id` recibe `403`.

## Reglas de permisos

- Dashboard global sigue bloqueado para `DRIVER`.
- OCR/review siguen bloqueados para `DRIVER`.
- Delivery events y evidence upload requieren ownership para `DRIVER`.

## Modelo User-Driver

`users.driver_id` referencia `drivers.id`, es nullable a nivel DB para no romper usuarios administrativos ni datos existentes. La obligatoriedad de `driver_id` para rol `DRIVER` se aplica en rutas/servicios.

## Metricas

- `driver_user_assignment_coverage`
- `driver_ownership_enforcement`
- `driver_forbidden_cross_access_count`
- `driver_operational_action_success_rate`
- `driver_unassigned_user_count`
- `permission_regression_test_pass_rate`

## Riesgos

- Usuarios DRIVER existentes pueden requerir backfill.
- Eventos historicos pueden tener `driver_id = null`.
- Ownership por orden/ruta sigue pendiente.

## Entregables

- Migracion Alembic.
- Modelo/schemas actualizados.
- Enforcement backend.
- Tests ownership.
- Docs y auditoria.

## Criterios de aceptacion

Ver `acceptance.md`.
