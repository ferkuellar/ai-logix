# AI Logix

Fase 1 incluye backend FastAPI + PostgreSQL + Docker.

Fase 2 agrega un frontend React + Vite con dashboard operativo, KPIs, tabla y mapa Leaflet para visualizar `GET /api/order-states`.

Fase 3 agrega subida local de evidencia fotografica y eventos `PHOTO_UPLOADED`.

Documentacion:

- [docs/fase-2-frontend-map.md](docs/fase-2-frontend-map.md)
- [docs/fase-3-subida-fotos.md](docs/fase-3-subida-fotos.md)

## Ejecucion

```bash
docker compose up --build
```

- Backend: `http://localhost:8000`
- Frontend: `http://localhost:5173`
