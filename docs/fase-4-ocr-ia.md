# Fase 4 - OCR / IA para evidencia fotografica

## Objetivo

Procesar una imagen ya subida como evidencia, extraer datos operativos del pedido y guardar el resultado en `delivery_events` sin mezclar OCR dentro del endpoint de upload.

No se implementa WhatsApp, app movil nativa, S3/R2 ni optimizacion de rutas.

## Flujo tecnico

1. El usuario sube una evidencia con `POST /api/evidence/upload`.
2. El backend valida content-type y magic bytes.
3. El backend guarda `/uploads/evidence/<filename>` y crea `PHOTO_UPLOADED`.
4. El frontend llama `POST /api/ocr/process/{event_id}`.
5. `ocr_service.py` busca el evento, resuelve la ruta local, valida magic bytes y llama al provider configurado.
6. El resultado se guarda en el mismo `delivery_event`:
   - `ocr_text`
   - `ai_extracted_json`
7. El usuario puede confirmar o corregir con `POST /api/ocr/confirm/{event_id}`.
8. La confirmacion marca `confirmed=true` y actualiza `order_states`.

## Endpoints

```http
POST /api/ocr/process/{event_id}
GET /api/ocr/result/{event_id}
POST /api/ocr/confirm/{event_id}
```

Ejemplo process:

```bash
curl -X POST http://localhost:8000/api/ocr/process/<EVENT_ID>
```

Ejemplo result:

```bash
curl -X GET http://localhost:8000/api/ocr/result/<EVENT_ID>
```

Ejemplo confirm:

```bash
curl -X POST http://localhost:8000/api/ocr/confirm/<EVENT_ID> \
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
    "observations": "Confirmado manualmente desde OCR"
  }'
```

## Variables de entorno

```bash
OCR_PROVIDER=mock
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4o-mini
```

## Mock provider

`OCR_PROVIDER=mock` no consume API externa. Devuelve texto OCR y JSON operativo simulado:

- `order_number`
- `store_code`
- `store_name`
- `barcode`
- `products`
- `status_suggestion`
- `observations`
- `confidence`
- `raw_text`

## OpenAI provider

`OCR_PROVIDER=openai` usa el SDK oficial `openai` y `OPENAI_API_KEY`. No hay secretos hardcodeados.

El provider esta preparado para enviar la imagen como data URL base64 al modelo configurado en `OPENAI_MODEL` usando entrada multimodal.

Si falta `OPENAI_API_KEY`, el backend devuelve error claro.

## Validacion magic bytes

La validacion minima no confia solo en extension ni content-type:

- JPEG: `FF D8 FF`
- PNG: `89 50 4E 47`
- WEBP: `RIFF....WEBP`

La validacion aplica al upload y al procesamiento OCR del archivo local.

## Autenticacion y roles

Esta fase deja preparado el diseno minimo sin bloquear OCR. No se implementa login todavia porque no existe tabla `users` ni dependencias de seguridad.

La siguiente fase recomendada debe implementar:

- JWT
- roles `ADMIN`, `SUPERVISOR`, `DRIVER`
- dependencies de autorizacion en FastAPI
- auditoria de accesos

## S3/R2 y retencion

El almacenamiento sigue siendo local para desarrollo. Para produccion:

- mover `uploads/evidence` a S3/R2
- guardar solo URLs o keys relativas
- firmar URLs cuando aplique
- definir retencion y purga de evidencia
- registrar checksum y tamano final

## Limitaciones

- OCR mock no interpreta la imagen real.
- OpenAI provider esta preparado, pero requiere API key y conectividad externa.
- No se crean eventos separados `OCR_PROCESSED`/`OCR_CONFIRMED`; se actualiza el evento original para evitar refactor grande de timeline.

## Riesgos

- Validacion magic bytes es minima, no antivirus.
- No hay autenticacion.
- No hay rate limit.
- No hay cola async; OCR corre en request/response.

## Recomendaciones para Fase 5

Fase 5 debe ser autenticacion, roles y permisos:

1. Agregar login con JWT.
2. Crear roles `ADMIN`, `SUPERVISOR`, `DRIVER`.
3. Proteger endpoints.
4. Restringir `DRIVER` a sus pedidos.
5. Permitir a `SUPERVISOR` ver rutas asignadas.
6. Permitir a `ADMIN` ver todo.
7. Agregar tabla `users`.
8. Hashear contrasenas con passlib/bcrypt.
9. Crear dependencies de autorizacion.
10. Ajustar frontend con login basico.
