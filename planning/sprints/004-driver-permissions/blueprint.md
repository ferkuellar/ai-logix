# Sprint 004 Blueprint - Driver Permissions

## Archivos a revisar

- `backend/app/models/user.py`
- `backend/app/models/driver.py`
- `backend/app/models/delivery_event.py`
- `backend/app/models/order_state.py`
- `backend/app/api/dependencies.py`
- `backend/app/api/routes.py`
- `backend/app/api/user_routes.py`
- `backend/app/schemas/`
- `backend/app/services/`
- `backend/tests/`
- `frontend/src/`
- `docs/API.md`
- `docs/DATA_MODEL.md`
- `docs/PERMISSIONS.md`

## Archivos a crear

- `backend/alembic/versions/20260517_0002_add_user_driver_relationship.py`
- `backend/tests/test_driver_ownership.py`
- `planning/sprints/004-driver-permissions/`
- `docs/auditoria-fase-4-driver-permissions.md`

## Archivos a modificar

- Modelos/schemas/rutas de backend.
- Tests existentes.
- Frontend auth/dashboard tests.
- Docs y planning.

## Plan tecnico

1. Agregar `users.driver_id`.
2. Crear migracion Alembic con FK e index.
3. Exponer `driver_id` en schemas de user/auth.
4. Validar `driver_id` en create/update de usuarios.
5. Agregar helpers de ownership en dependencies.
6. Resolver `driver_id` para delivery events y evidence upload.
7. Asociar event/order state con driver resuelto.
8. Agregar tests backend y frontend.
9. Validar suites.
10. Actualizar docs/auditoria.

## Estrategia de migracion

La migracion agrega columna nullable para preservar datos existentes. La regla obligatoria para `DRIVER` se aplica en la aplicacion.

## Estrategia de validacion

- `python -m pytest backend/tests`
- `docker compose exec backend python -m pytest`
- `npm run test`
- `npm run build`
- `npm run lint`
- `docker compose config`
- Alembic history/current/upgrade o bloqueo documentado.

## Rollback

Usar downgrade de la migracion para eliminar FK, index y columna. Revertir cambios de rutas/schemas/tests si se revierte la fase.

## Riesgos

- Backfill de usuarios DRIVER existentes.
- Eventos historicos sin driver.
- Sin asignacion formal por orden/ruta.

## No-go items

- No cambiar reglas de negocio fuera de ownership DRIVER.
- No crear endpoint DRIVER amplio sin definicion de producto.
- No relajar permisos para pasar tests.
