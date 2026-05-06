# Fase 6 - Autenticacion, roles y permisos

## Objetivo

Agregar autenticacion JWT, usuarios, roles operativos, proteccion de endpoints y auditoria minima de acciones criticas.

No se implementa WhatsApp, S3/R2, app movil nativa ni optimizacion avanzada de rutas.

## Roles

- `ADMIN`: acceso total, gestion de usuarios y operacion.
- `SUPERVISOR`: dashboard, evidencias, OCR y revision humana.
- `DRIVER`: subida de evidencia y eventos operativos propios. No accede a dashboard global, OCR administrativo ni revision humana.

## Endpoints publicos

```http
GET /api/health
POST /api/auth/login
```

## Endpoints protegidos

```http
GET /api/auth/me
GET /api/users
POST /api/users
GET /api/users/{user_id}
PATCH /api/users/{user_id}
DELETE /api/users/{user_id}
GET /api/order-states
POST /api/delivery-events
POST /api/evidence/upload
POST /api/ocr/process/{event_id}
GET /api/ocr/result/{event_id}
POST /api/ocr/confirm/{event_id}
GET /api/review/pending
GET /api/review/{event_id}
POST /api/review/{event_id}/confirm
POST /api/review/{event_id}/reject
```

## Reglas de acceso por rol

| Endpoint | ADMIN | SUPERVISOR | DRIVER |
| --- | --- | --- | --- |
| `/api/users*` | Si | No | No |
| `/api/order-states` | Si | Si | No |
| `/api/delivery-events` | Si | Si | Si |
| `/api/evidence/upload` | Si | Si | Si |
| `/api/ocr/*` | Si | Si | No |
| `/api/review/*` | Si | Si | No |

## Variables de entorno

```bash
SECRET_KEY=change-me-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

SEED_ADMIN_EMAIL=admin@ailogix.local
SEED_ADMIN_PASSWORD=ChangeMe123!
SEED_ADMIN_NAME=System Admin
```

`SECRET_KEY` debe cambiarse en produccion y gestionarse como secreto.

## Seed de admin

Con el sistema levantado:

```bash
docker compose exec backend python -m app.scripts.seed_admin
```

El script crea el usuario si no existe:

- email: `admin@ailogix.local`
- password: `ChangeMe123!`
- role: `ADMIN`

## Flujo de login frontend

1. El usuario abre `http://localhost:5173`.
2. Si no hay token, se muestra `Login`.
3. El frontend llama `POST /api/auth/login`.
4. Guarda token y usuario en `localStorage`.
5. Axios agrega `Authorization: Bearer <token>`.
6. Si el backend responde 401, se limpia sesion.
7. Las vistas se filtran por rol.

## Auditoria de accesos

Se registra `AuditLog` en:

- login exitoso
- login fallido
- subida de evidencia
- procesamiento OCR
- confirmacion de revision humana
- rechazo de revision humana
- creacion de usuario
- desactivacion de usuario

Campos:

- `user_id`
- `action`
- `resource_type`
- `resource_id`
- `metadata_json`
- `ip_address`
- `created_at`

## Limitaciones

- No hay migraciones formales; se mantiene `Base.metadata.create_all`.
- `DRIVER` todavia no filtra por relacion `user_id`/`driver_id` porque el modelo no tiene esa relacion.
- El token se guarda en `localStorage`, suficiente para desarrollo pero no ideal para produccion de alta seguridad.
- No hay refresh tokens.
- No hay recuperacion de contrasena.

## Riesgos

- `SECRET_KEY` por defecto solo es seguro para desarrollo.
- Sin tabla que vincule `User` con `Driver`, la restriccion DRIVER queda limitada a permisos por endpoint.
- No hay rate limit en login.
- No hay bloqueo por intentos fallidos.

## Recomendaciones para siguiente fase

Fase 7 debe ser vista mobile-first para repartidor:

1. Crear vista especifica para `DRIVER`.
2. Relacionar `users` con `drivers`.
3. Mostrar solo pedidos asignados.
4. Permitir subida rapida de evidencia desde celular.
5. Capturar geolocalizacion del navegador.
6. Agregar acciones grandes para uso en campo.
7. Preparar retry manual y manejo de baja conectividad.
