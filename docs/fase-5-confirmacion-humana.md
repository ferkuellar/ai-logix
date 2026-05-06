# Fase 5 - Confirmacion humana del OCR

## Objetivo

Convertir el OCR/IA en una sugerencia operativa que debe ser revisada por una persona antes de considerarse confiable.

No se implementa autenticacion, WhatsApp, app movil nativa ni S3/R2.

## Por que OCR no es fuente de verdad

El OCR puede fallar por imagen borrosa, mala iluminacion, texto cortado, etiquetas mal impresas o inferencias incorrectas del modelo. Por eso el flujo separa dos conceptos:

- OCR = sugerencia.
- Confirmacion humana = dato operativo confiable.

## Flujo de revision humana

1. El usuario sube evidencia con `POST /api/evidence/upload`.
2. Se procesa OCR con `POST /api/ocr/process/{event_id}`.
3. El resultado queda con `review_status=HUMAN_REVIEW_REQUIRED`.
4. La cola `GET /api/review/pending` muestra eventos no confirmados.
5. El supervisor consulta detalle con `GET /api/review/{event_id}`.
6. El supervisor confirma o corrige con `POST /api/review/{event_id}/confirm`.
7. Si la imagen no es confiable, rechaza con `POST /api/review/{event_id}/reject`.

## Estados de revision

Los estados se guardan dentro de `delivery_events.ai_extracted_json.review_status`:

- `OCR_PENDING`
- `OCR_PROCESSED`
- `HUMAN_REVIEW_REQUIRED`
- `HUMAN_CONFIRMED`
- `HUMAN_REJECTED`

Deuda tecnica: estos estados deberian vivir en una columna dedicada o en eventos separados cuando se incorpore una migracion formal.

## Endpoints agregados

```http
GET /api/review/pending
GET /api/review/{event_id}
POST /api/review/{event_id}/confirm
POST /api/review/{event_id}/reject
```

`GET /api/review/pending` acepta filtros:

- `status`
- `order_number`
- `limit`
- `offset`

## Payloads de ejemplo

Confirmar:

```bash
curl -X POST http://localhost:8000/api/review/<EVENT_ID>/confirm \
  -H "Content-Type: application/json" \
  -d '{
    "order_number": "PED-0001",
    "store_code": "OX-CHIH-001",
    "store_name": "OXXO Centro",
    "barcode": "7501234567890",
    "products": [
      {
        "name": "Producto demo",
        "quantity": 2
      }
    ],
    "status": "DELIVERED",
    "latitude": 28.6353,
    "longitude": -106.0889,
    "observations": "Confirmado manualmente despues de OCR"
  }'
```

Rechazar:

```bash
curl -X POST http://localhost:8000/api/review/<EVENT_ID>/reject \
  -H "Content-Type: application/json" \
  -d '{
    "reason": "La imagen esta borrosa y el OCR no es confiable",
    "observations": "Solicitar nueva foto al repartidor"
  }'
```

## Impacto sobre order_states

Solo la confirmacion humana actualiza `order_states`.

Al confirmar:

- actualiza `delivery_events.order_number`
- actualiza `delivery_events.status`
- actualiza `delivery_events.latitude`
- actualiza `delivery_events.longitude`
- guarda `confirmed_data`
- marca `confirmed=true`
- marca `review_status=HUMAN_CONFIRMED`
- crea o actualiza `order_states`

Al rechazar:

- marca `review_status=HUMAN_REJECTED`
- guarda `rejection_reason`
- guarda `rejected_at`
- no marca el pedido como entregado
- no actualiza `order_states` como dato confiable

## Frontend

La vista `/review` muestra:

- cola de eventos pendientes
- foto de evidencia
- texto OCR
- JSON extraido
- formulario editable de confirmacion
- formulario de rechazo con razon obligatoria

## Limitaciones

- No hay autenticacion ni roles.
- No hay auditoria por usuario.
- No hay eventos separados `HUMAN_CONFIRMED` o `HUMAN_REJECTED`; se guarda el resultado en el mismo `delivery_event`.
- No hay migraciones de base de datos.

## Riesgos

- Cualquier usuario con acceso al backend puede confirmar/rechazar mientras no exista auth.
- La cola filtra en memoria el estado de revision porque `review_status` vive en JSON.
- Sin worker async, OCR sigue siendo request/response.

## Recomendaciones para la siguiente fase

Fase 6 debe ser autenticacion, roles y permisos:

1. Agregar JWT.
2. Crear roles `ADMIN`, `SUPERVISOR`, `DRIVER`.
3. Crear tabla `users`.
4. Hashear contrasenas con `passlib`/`bcrypt`.
5. Crear endpoints `POST /api/auth/login` y `GET /api/auth/me`.
6. Crear dependencies `get_current_user`, `require_role` y `require_admin`.
7. Proteger evidencia, OCR, revision humana y estados.
8. Agregar login basico en frontend.
9. Agregar interceptor Axios.
10. Registrar auditoria de accesos.
