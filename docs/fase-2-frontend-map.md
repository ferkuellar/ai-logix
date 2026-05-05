# Fase 2 - Frontend React con mapa operativo

Esta fase agrega un frontend React + Vite en `frontend/` para consultar `GET /api/order-states` y visualizar el estado operativo de entregas OXXO en KPIs, mapa Leaflet y tabla.

## Stack

- React + Vite
- TailwindCSS
- Leaflet + react-leaflet
- Axios
- Docker integrado a `docker-compose.yml`

## Variables de entorno

El frontend lee la URL base del backend desde:

```bash
VITE_API_BASE_URL=http://localhost:8000/api
```

Si no se define, usa `http://localhost:8000/api`.

Si el frontend ya estaba corriendo antes de instalar TailwindCSS o crear `postcss.config.js`, reinicia el servidor de Vite para que cargue la configuracion de PostCSS:

```bash
cd frontend
npm run dev
```

El backend permite CORS desde `http://localhost:5173` y `http://127.0.0.1:5173` por defecto. Se puede sobrescribir con:

```bash
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

## Ejecucion local

```bash
cd frontend
npm install
npm run dev
```

Frontend: `http://localhost:5173`

Backend esperado: `http://localhost:8000`

## Ejecucion con Docker

```bash
docker compose up --build
```

Servicios:

- PostgreSQL: `localhost:5432`
- Backend: `http://localhost:8000`
- Frontend: `http://localhost:5173`

## Pruebas rapidas

Health check:

```bash
curl http://localhost:8000/api/health
```

Consultar estados:

```bash
curl http://localhost:8000/api/order-states
```

Insertar eventos de prueba:

```bash
curl -X POST http://localhost:8000/api/delivery-events \
  -H "Content-Type: application/json" \
  -d "{\"event_type\":\"DELIVERY_STATUS\",\"order_number\":\"OX-1001\",\"status\":\"DELIVERED\",\"latitude\":25.6866,\"longitude\":-100.3161,\"observations\":\"Entrega completa\"}"
```

```bash
curl -X POST http://localhost:8000/api/delivery-events \
  -H "Content-Type: application/json" \
  -d "{\"event_type\":\"DELIVERY_STATUS\",\"order_number\":\"OX-1002\",\"status\":\"PENDING\",\"latitude\":25.6743,\"longitude\":-100.3090,\"observations\":\"Pendiente de surtido\"}"
```

```bash
curl -X POST http://localhost:8000/api/delivery-events \
  -H "Content-Type: application/json" \
  -d "{\"event_type\":\"DELIVERY_STATUS\",\"order_number\":\"OX-1003\",\"status\":\"FAILED\",\"latitude\":25.7002,\"longitude\":-100.3304,\"observations\":\"No atendido\"}"
```

## Criterios visuales

- `DELIVERED`: verde
- `PARTIAL`: amarillo
- `PENDING`: amarillo
- `FAILED`: rojo
- `CANCELLED`: rojo

## Ajustes minimos a Fase 1

- Se agrego CORS al backend para permitir llamadas desde el frontend local.
- Se actualiza `last_update_at` cada vez que un evento modifica un `OrderState`.
