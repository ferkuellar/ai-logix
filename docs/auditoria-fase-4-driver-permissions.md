# Auditoria Fase 4 - Driver Permissions

## 1. Resumen ejecutivo

Fase 4 queda completa para el alcance definido. AI Logix ahora tiene relacion formal `User.driver_id -> Driver.id` y reglas de ownership que impiden que un usuario `DRIVER` opere recursos de otro repartidor.

## 2. Auditoria inicial de permisos DRIVER

Antes de Fase 4, `DRIVER` tenia acceso por endpoint a crear eventos y subir evidencia, pero no existia asociacion formal entre usuario autenticado y registro `Driver`.

## 3. Brechas detectadas

- `users.driver_id` no existia.
- Usuarios DRIVER podian operar sin identidad de repartidor.
- Delivery events aceptaban `driver_id` sin validar ownership.
- Evidence upload no asociaba evidencia al driver autenticado.
- Frontend no tenia regresion para dashboard bloqueado a DRIVER.

## 4. Decisiones de diseno

- `User.driver_id` es la relacion formal usuario-repartidor.
- `DRIVER` requiere `driver_id` para acciones operativas.
- `ADMIN` y `SUPERVISOR` retienen alcance global.
- Fase 4 controla ownership por driver, no por orden/ruta.
- Vista mobile-first DRIVER queda fuera de alcance.

## 5. Plan tecnico aplicado

- Agregar modelo/schemas con `driver_id`.
- Agregar migracion Alembic.
- Validar usuarios DRIVER en create/update.
- Agregar helpers de ownership.
- Resolver `driver_id` en delivery events/evidence upload.
- Asociar eventos y order states al driver resuelto.
- Agregar tests backend y frontend.
- Actualizar docs y planning.

## 6. Archivos creados

- `backend/alembic/versions/20260517_0002_add_user_driver_relationship.py`
- `backend/tests/test_driver_ownership.py`
- `planning/sprints/004-driver-permissions/requirements.md`
- `planning/sprints/004-driver-permissions/blueprint.md`
- `planning/sprints/004-driver-permissions/acceptance.md`
- `planning/sprints/004-driver-permissions/handoff-prompt.md`
- `docs/auditoria-fase-4-driver-permissions.md`

## 7. Archivos modificados

- `backend/app/models/user.py`
- `backend/app/schemas/user.py`
- `backend/app/schemas/auth.py`
- `backend/app/services/auth_service.py`
- `backend/app/services/evidence_service.py`
- `backend/app/api/dependencies.py`
- `backend/app/api/routes.py`
- `backend/app/api/user_routes.py`
- `backend/tests/conftest.py`
- `backend/tests/test_alembic_config.py`
- `frontend/src/__tests__/App.test.jsx`
- `frontend/src/__tests__/Login.test.jsx`
- `docs/API.md`
- `docs/DATA_MODEL.md`
- `docs/PERMISSIONS.md`
- `docs/VALIDATION.md`
- `docs/OPERATIONS.md`
- `docs/METRICS.md`
- `planning/STATE.md`
- `planning/DECISIONS.md`
- `planning/RISKS.md`
- `planning/QUESTIONS.md`
- `planning/METRICS.md`
- `README.md`

## 8. Migracion creada

`backend/alembic/versions/20260517_0002_add_user_driver_relationship.py`

Incluye:

- `users.driver_id`
- index `ix_users_driver_id`
- FK `users.driver_id -> drivers.id`
- downgrade que elimina FK, index y columna

## 9. Cambios de modelo de datos

- `User.driver_id` nullable con FK a `Driver`.
- `User.driver` relationship.
- `CurrentUserResponse` y `UserResponse` exponen `driver_id`.
- La obligatoriedad para `DRIVER` se aplica en la app para preservar datos existentes.

## 10. Cambios de API/permisos

- `POST /api/users`: DRIVER requiere `driver_id` valido.
- `PATCH /api/users/{user_id}`: el resultado DRIVER requiere `driver_id` valido.
- `POST /api/delivery-events`: DRIVER solo usa su `driver_id`; si lo omite se asigna automaticamente.
- `POST /api/evidence/upload`: DRIVER solo sube evidencia propia; el evento queda asociado a su driver.
- `ADMIN`/`SUPERVISOR`: pueden operar para cualquier `driver_id` valido.
- `DRIVER`: sigue bloqueado en dashboard global, OCR y review.

## 11. Tests backend agregados

- `backend/tests/test_driver_ownership.py`
- Tests Alembic extendidos para migracion y `users.driver_id`.
- Fixture `driver_user` ahora crea un `Driver` asociado.

## 12. Tests frontend agregados o justificacion

- `App.test.jsx` agrega regresion para usuario `DRIVER` autenticado: dashboard global queda bloqueado.
- `Login.test.jsx` acepta `driver_id` en auth state.

No se redisenaron vistas; Fase 4 no crea mobile-first driver UX.

## 13. Validaciones ejecutadas

| Command | Result |
| --- | --- |
| `docker compose config` | Passed |
| `docker compose exec backend alembic -c alembic.ini history` | Passed |
| `docker compose exec backend alembic -c alembic.ini current` before adoption | Passed with note: no revision displayed because DB predated Alembic |
| `docker compose exec backend alembic -c alembic.ini upgrade head` before adoption | Documented failure: duplicate `drivers` table from pre-Alembic local DB |
| `docker compose exec backend alembic -c alembic.ini stamp 20260517_0001` | Passed; local baseline adopted |
| `docker compose exec backend alembic -c alembic.ini upgrade head` after adoption | Passed; upgraded to `20260517_0002` |
| `docker compose exec backend alembic -c alembic.ini current` after upgrade | Passed; `20260517_0002 (head)` |
| `python -m pytest backend/tests` | Passed, 66 tests |
| `docker compose exec backend python -m pytest` | Passed, 66 tests |
| `cd frontend && npm run test` | Passed, 9 tests |
| `cd frontend && npm run build` | Passed |
| `cd frontend && npm run lint` | Passed |

## 14. Riesgos restantes

- Usuarios DRIVER existentes pueden requerir backfill de `driver_id`.
- Eventos historicos pueden tener `driver_id = null`.
- No hay asignacion formal orden-driver.
- No hay endpoint scoped para vista DRIVER.
- Evidence access y retention siguen pendientes.

## 15. Preguntas abiertas

- Como se backfillan usuarios DRIVER existentes sin `driver_id`?
- Debe existir tabla formal de asignacion orden-driver?
- Que endpoint scoped necesita el DRIVER para su vista operativa?

## 16. Acceptance final

Todos los criterios de `planning/sprints/004-driver-permissions/acceptance.md` estan completos, con validaciones o bloqueos documentados.

## 17. Auditoria final

Fase 4 cierra la brecha principal de ownership DRIVER a nivel backend. La seguridad queda basada en `driver_id`, con rutas criticas cubiertas por tests. La siguiente brecha logica es proteger evidencia y definir retencion.

## 18. Siguiente fase recomendada

Fase 5 - Evidencia protegida y politica de retencion.

## 19. Commit sugerido

```text
security: enforce driver ownership and operational assignment
```
