# Auditoria Fase 2 - Alembic Data Model

## 1. Resumen ejecutivo

Fase 2 queda completa para el alcance definido: Alembic fue integrado como herramienta formal de migraciones, se creo una migracion baseline del schema actual, `create_all` quedo restringido a compatibilidad local de desarrollo, y la documentacion operativa/modelo de datos fue actualizada.

La validacion detecto una condicion esperada: la base local existente ya tenia tablas creadas por `create_all`, por lo que `alembic upgrade head` no puede aplicar la baseline sobre esa DB sin una adopcion previa. La accion correcta es comparar schema y ejecutar `alembic stamp head`, o recrear la DB local y aplicar migraciones antes del arranque de la app.

## 2. Auditoria inicial

- Fase 0 y Fase 1 estaban presentes antes de modificar codigo.
- El repo no tenia carpeta anidada `ai-logix/ai-logix`.
- El backend usaba SQLAlchemy models y arranque local con `Base.metadata.create_all`.
- No existia estructura Alembic formal.
- El riesgo principal era evolucionar schema sin historial auditable.

## 3. Brechas detectadas

- No habia `backend/alembic.ini`.
- No habia `backend/alembic/env.py`.
- No habia carpeta `backend/alembic/versions`.
- No habia migracion baseline.
- `Base.metadata.create_all` podia crear tablas sin migracion.
- Bases existentes creadas antes de Alembic no tienen `alembic_version`.
- `User` no tiene relacion formal con `Driver`.
- No existe tabla formal `orders`; el sistema usa `order_number`.
- Algunos campos JSON flexibles pueden dificultar validacion y reporting.

## 4. Plan tecnico aplicado

- Agregar dependencia `alembic`.
- Crear configuracion Alembic bajo `backend/`.
- Hacer que Alembic lea `settings.database_url`.
- Importar todos los modelos actuales en `env.py`.
- Crear baseline manual revisada contra los modelos SQLAlchemy actuales.
- Restringir `Base.metadata.create_all` a `APP_ENV=development`.
- Documentar politica de migraciones, rollback, backup y adopcion de baseline.
- Actualizar riesgos, decisiones, metricas, estado y sprint 002.

## 5. Archivos creados

- `backend/alembic.ini`
- `backend/alembic/env.py`
- `backend/alembic/script.py.mako`
- `backend/alembic/versions/20260517_0001_baseline_schema.py`
- `backend/tests/test_alembic_config.py`
- `docs/DATABASE_MIGRATIONS.md`
- `docs/auditoria-fase-2-alembic-data-model.md`
- `planning/sprints/002-alembic-data-model/requirements.md`
- `planning/sprints/002-alembic-data-model/blueprint.md`
- `planning/sprints/002-alembic-data-model/acceptance.md`
- `planning/sprints/002-alembic-data-model/handoff-prompt.md`

## 6. Archivos modificados

- `backend/requirements.txt`
- `backend/app/main.py`
- `backend/app/core/config.py`
- `docs/DATA_MODEL.md`
- `docs/OPERATIONS.md`
- `docs/VALIDATION.md`
- `docs/METRICS.md`
- `planning/STATE.md`
- `planning/DECISIONS.md`
- `planning/RISKS.md`
- `planning/QUESTIONS.md`
- `planning/METRICS.md`
- `README.md`

## 7. Migracion baseline creada

Archivo:

```text
backend/alembic/versions/20260517_0001_baseline_schema.py
```

Tablas cubiertas:

- `drivers`
- `stores`
- `users`
- `audit_logs`
- `delivery_events`
- `order_states`

La migracion incluye `upgrade()` y `downgrade()`, constraints de unicidad verificadas, indices existentes y foreign keys detectadas en los modelos.

## 8. Revision del modelo de datos

`docs/DATA_MODEL.md` fue actualizado con:

- Proposito por entidad.
- Primary key.
- Campos importantes detectados.
- Relaciones implementadas.
- Brechas de relacion.
- Riesgos e impactos.
- Mejoras futuras.

Brechas principales:

- `User` y `Driver` no tienen relacion formal.
- `OrderState` depende de `order_number` sin tabla `orders`.
- Estados oficiales de orden no estan formalizados como catalogo.
- Campos JSON de OCR/review requieren contrato antes de reporting fuerte.

## 9. Validaciones ejecutadas

| Command | Result | Notes |
| --- | --- | --- |
| `docker compose config` | Passed | Compose renderizo configuracion valida. |
| `python -m pytest backend/tests/test_alembic_config.py` | Passed | 3 tests passed. |
| `python -m pytest backend/tests` | Passed | 34 tests passed. |
| `cd backend; python -m alembic -c alembic.ini history` | Passed | Baseline visible. |
| `docker compose up --build -d` | Passed | Stack local construido e iniciado. |
| `docker compose exec backend alembic -c alembic.ini history` | Passed | Baseline visible dentro del contenedor. |
| `docker compose exec backend alembic -c alembic.ini current` | Passed with note | No mostro revision porque la DB local no esta stamped. |
| `docker compose exec backend alembic -c alembic.ini upgrade head` | Blocked/documented | Falla por tabla `drivers` existente en DB creada antes de Alembic. |
| `docker compose exec backend pytest` | Failed/documented | `ModuleNotFoundError: No module named 'app'`; usar `python -m pytest`. |
| `docker compose exec backend python -m pytest` | Passed | 34 tests passed. |

## 10. Tests ejecutados

- `backend/tests/test_alembic_config.py`: valida presencia de Alembic, baseline y metadata esperada.
- Suite backend completa local: 34 tests passed.
- Suite backend completa en Docker con `python -m pytest`: 34 tests passed.

## 11. Riesgos restantes

- DBs existentes creadas con `create_all` requieren comparacion y `alembic stamp head` antes de continuar con migraciones.
- `create_all` sigue activo solo en development por compatibilidad local temporal.
- Migraciones aun no estan automatizadas en CI/CD.
- Backup/restore no esta implementado.
- `User` y `Driver` no tienen relacion formal.
- No existe tabla formal `orders`.
- Downgrades futuros pueden ser limitados si transforman o eliminan datos.
- Indices adicionales deben definirse con base en consultas reales.

## 12. Preguntas abiertas

- Existing databases creadas con `create_all` deben ser stamped o recreadas localmente?
- Que indices se necesitan para consultas frecuentes de `delivery_events` y `audit_logs`?
- Cuando se formalizara una tabla `orders`?
- Cuales son los estados oficiales de una orden?
- Como se asignan ordenes a drivers?

## 13. Acceptance final

Todos los criterios de `planning/sprints/002-alembic-data-model/acceptance.md` estan completos. Los criterios de ejecucion de Alembic fueron ejecutados o tienen bloqueo documentado con causa, impacto y siguiente accion.

## 14. Auditoria final

Fase 2 cumple el objetivo de reducir riesgo de cambios destructivos o inconsistentes en el schema. Alembic queda como mecanismo oficial, la baseline existe, la politica operativa esta documentada y los riesgos residuales son visibles.

La unica limitacion operativa inmediata esta en la DB local existente, no en la integracion de Alembic: esa DB debe adoptarse con `stamp head` tras comparacion de schema, o recrearse para aplicar la baseline desde cero.

## 15. Siguiente fase recomendada

Fase 3 - Tests criticos backend/frontend.

## 16. Commit sugerido

```text
database: add Alembic migrations and baseline schema
```
