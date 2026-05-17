# AI Logix

Fase 1 incluye backend FastAPI + PostgreSQL + Docker.

Fase 2 agrega un frontend React + Vite con dashboard operativo, KPIs, tabla y mapa Leaflet para visualizar `GET /api/order-states`.

Fase 3 agrega subida local de evidencia fotografica y eventos `PHOTO_UPLOADED`.

Fase 4 agrega OCR/IA desacoplado para procesar evidencia, con mock provider local y provider OpenAI preparado.

Fase 5 agrega revision humana del OCR para confirmar o rechazar datos antes de actualizar el estado operativo confiable.

Fase 6 agrega autenticacion JWT, roles `ADMIN`/`SUPERVISOR`/`DRIVER`, proteccion de endpoints operativos y auditoria minima.

Axon-AI Fase 4 agrega ownership operativo para `DRIVER`: cada usuario repartidor debe tener `driver_id`, solo puede crear eventos/subir evidencia para su propio repartidor, y `ADMIN`/`SUPERVISOR` mantienen alcance operativo global.

Documentacion:

- [docs/SECURITY.md](docs/SECURITY.md)
- [docs/OPERATIONS.md](docs/OPERATIONS.md)
- [docs/VALIDATION.md](docs/VALIDATION.md)
- [docs/TESTING.md](docs/TESTING.md)
- [docs/DATABASE_MIGRATIONS.md](docs/DATABASE_MIGRATIONS.md)
- [docs/fase-2-frontend-map.md](docs/fase-2-frontend-map.md)
- [docs/fase-3-subida-fotos.md](docs/fase-3-subida-fotos.md)
- [docs/fase-4-ocr-ia.md](docs/fase-4-ocr-ia.md)
- [docs/fase-5-confirmacion-humana.md](docs/fase-5-confirmacion-humana.md)
- [docs/fase-6-auth-roles-permisos.md](docs/fase-6-auth-roles-permisos.md)

## Ejecucion

```bash
docker compose up --build
```

- Backend: `http://localhost:8000`
- Frontend: `http://localhost:5173`

## Configuracion

Crear `.env` desde `.env.example` y no subir `.env` al repositorio.

En ambientes fuera de `development`, la app bloquea configuraciones inseguras:

- `SECRET_KEY` default, vacio o menor a 32 caracteres.
- `SEED_ADMIN_PASSWORD` default, vacio o menor a 12 caracteres.
- `CORS_ORIGINS=*`.
- `DATABASE_URL` faltante.

## Seed admin

```bash
docker compose exec backend python -m app.scripts.seed_admin
```

Login desarrollo:

- Email: `admin@ailogix.local`
- Password: `ChangeMe123!`

## Migraciones

Alembic vive en `backend/`.

```bash
docker compose exec backend alembic -c alembic.ini current
docker compose exec backend alembic -c alembic.ini history
docker compose exec backend alembic -c alembic.ini upgrade head
```

Si una base local fue creada antes de Alembic con tablas existentes, adoptar primero la baseline de desarrollo y luego aplicar head:

```bash
docker compose exec backend alembic -c alembic.ini stamp 20260517_0001
docker compose exec backend alembic -c alembic.ini upgrade head
```

## Tests

Backend:

```bash
python -m pytest backend/tests
docker compose exec backend python -m pytest
```

Frontend:

```bash
cd frontend
npm install
npm run test
npm run build
npm run lint
```
