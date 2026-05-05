# Fase 3 - Subida de fotos / evidencia fotografica

Esta fase agrega carga de evidencia fotografica sin OCR, WhatsApp ni autenticacion. El almacenamiento es local para desarrollo.

## Backend

Endpoint:

```http
POST /api/evidence/upload
```

Campos `multipart/form-data`:

- `file`: imagen JPG, PNG o WEBP
- `order_number`: string requerido
- `status`: string opcional
- `latitude`: float opcional
- `longitude`: float opcional
- `observations`: string opcional

Validaciones:

- Tipos permitidos: `image/jpeg`, `image/png`, `image/webp`
- Tamano maximo: 10 MB
- Nombre seguro: `evidence_<uuid>.<ext>`
- URL publica relativa: `/uploads/evidence/<filename>`

El endpoint crea un evento `PHOTO_UPLOADED` en `delivery_events` y actualiza `order_states` para el pedido enviado.

## Frontend

Vista:

```text
http://localhost:5173/evidence
```

La vista permite capturar datos del pedido, seleccionar imagen, ver preview, subir evidencia y abrir la URL resultante.

## Docker

`docker-compose.yml` monta:

```yaml
./backend/uploads:/app/uploads
```

Esto mantiene persistentes las evidencias locales durante desarrollo.

## Ejecucion

```bash
docker compose up --build
```

Backend:

```text
http://localhost:8000/docs
```

Frontend:

```text
http://localhost:5173
```

## Ejemplo curl

```bash
curl -X POST http://localhost:8000/api/evidence/upload \
  -F "order_number=OX-3001" \
  -F "status=DELIVERED" \
  -F "latitude=25.6866" \
  -F "longitude=-100.3161" \
  -F "observations=Foto de evidencia de entrega" \
  -F "file=@./evidence-test.jpg;type=image/jpeg"
```

## Ejemplo PowerShell

```powershell
$filePath = ".\evidence-test.jpg"
$fileStream = [System.IO.File]::OpenRead($filePath)
$fileContent = [System.Net.Http.StreamContent]::new($fileStream)
$fileContent.Headers.ContentType = [System.Net.Http.Headers.MediaTypeHeaderValue]::Parse("image/jpeg")

$multipart = [System.Net.Http.MultipartFormDataContent]::new()
$multipart.Add([System.Net.Http.StringContent]::new("OX-3001"), "order_number")
$multipart.Add([System.Net.Http.StringContent]::new("DELIVERED"), "status")
$multipart.Add([System.Net.Http.StringContent]::new("25.6866"), "latitude")
$multipart.Add([System.Net.Http.StringContent]::new("-100.3161"), "longitude")
$multipart.Add([System.Net.Http.StringContent]::new("Foto de evidencia de entrega"), "observations")
$multipart.Add($fileContent, "file", [System.IO.Path]::GetFileName($filePath))

try {
  Invoke-RestMethod -Uri "http://localhost:8000/api/evidence/upload" -Method Post -Body $multipart
}
finally {
  $multipart.Dispose()
  $fileStream.Dispose()
}
```

## Prueba en navegador

1. Levanta el stack con `docker compose up --build`.
2. Abre `http://localhost:5173/evidence`.
3. Captura `order_number`.
4. Selecciona `status` si quieres actualizar el pedido.
5. Agrega coordenadas y observaciones si aplican.
6. Selecciona una imagen JPG, PNG o WEBP menor a 10 MB.
7. Verifica el preview.
8. Presiona `Subir evidencia`.
9. Abre la URL devuelta por el formulario.
10. Regresa al dashboard y valida que `order_states` refleje el pedido.

## Fuera de alcance

- OCR
- WhatsApp
- Autenticacion
- S3/R2 u otro almacenamiento remoto
