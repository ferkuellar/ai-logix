# Sprint 003 Blueprint - Critical Tests

## Archivos a revisar

- `backend/tests/`
- `backend/app/api/`
- `backend/app/services/`
- `frontend/package.json`
- `frontend/vite.config.js`
- `frontend/src/`
- `docs/VALIDATION.md`
- `docs/OPERATIONS.md`
- `planning/STATE.md`
- `planning/RISKS.md`
- `planning/METRICS.md`

## Archivos a crear

- `backend/tests/test_health.py`
- `backend/tests/test_auth.py`
- `backend/tests/test_permissions.py`
- `backend/tests/test_delivery_events.py`
- `backend/tests/test_audit_log.py`
- `frontend/src/test/setup.js`
- `frontend/src/__tests__/App.test.jsx`
- `frontend/src/__tests__/Login.test.jsx`
- `frontend/src/__tests__/Dashboard.test.jsx`
- `docs/TESTING.md`
- `docs/auditoria-fase-3-critical-tests.md`
- Sprint docs bajo `planning/sprints/003-critical-tests/`

## Archivos a modificar

- `backend/tests/conftest.py`
- `backend/tests/test_evidence_upload.py`
- `backend/tests/test_ocr_flow.py`
- `frontend/package.json`
- `frontend/package-lock.json`
- `frontend/vite.config.js`
- `docs/VALIDATION.md`
- `docs/OPERATIONS.md`
- `docs/METRICS.md`
- `planning/STATE.md`
- `planning/DECISIONS.md`
- `planning/RISKS.md`
- `planning/METRICS.md`
- `README.md`

## Estrategia backend

- Mantener `pytest` como framework oficial.
- Reusar `TestClient` y fixtures existentes.
- Usar SQLite in-memory para suite rapida.
- Forzar `OCR_PROVIDER=mock`.
- Crear usuarios por rol con helpers existentes.
- Limpiar uploads temporales antes y despues de cada test.
- Agregar tests de brechas criticas sin duplicar innecesariamente.

## Estrategia frontend

- Agregar Vitest + Testing Library + jsdom.
- Mockear API client para no depender del backend.
- Mockear `react-leaflet` para evitar dependencia de DOM/map real.
- Validar login, persistencia de sesion, limpieza por 401/evento y dashboard.

## Plan paso a paso

1. Ejecutar precheck de fases previas.
2. Auditar tests backend existentes.
3. Agregar tests backend faltantes.
4. Agregar limpieza de uploads en fixture global.
5. Agregar tooling frontend.
6. Agregar tests frontend minimos.
7. Ejecutar backend tests local y Docker.
8. Ejecutar frontend test/build/lint.
9. Actualizar docs, metricas, riesgos y estado.
10. Completar auditoria y acceptance.

## Validacion

- `docker compose config`
- `python -m pytest backend/tests`
- `docker compose exec backend python -m pytest`
- `cd frontend && npm install`
- `cd frontend && npm run test`
- `cd frontend && npm run build`
- `cd frontend && npm run lint`

## Riesgos

- Warnings existentes pueden ocultar fallos futuros si crecen.
- Frontend tests no reemplazan validacion visual/manual.
- Suite critica no equivale a cobertura total.

## Rollback

- Revertir archivos de tests y dependencias frontend agregadas.
- Restaurar `frontend/package.json`, `frontend/package-lock.json` y `vite.config.js`.
- Restaurar `backend/tests/conftest.py` si la limpieza de uploads causa efecto no deseado.

## No-go items

- No llamar OpenAI real.
- No cambiar reglas de negocio.
- No agregar E2E pesado.
- No modificar permisos productivos para hacer pasar tests.
