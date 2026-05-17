# Sprint 001 Requirements - Security Configuration

## Problema

AI Logix permitia valores default inseguros en configuracion runtime. Esos valores son aceptables en desarrollo local, pero no deben permitir que una instancia no-development arranque con `SECRET_KEY`, `SEED_ADMIN_PASSWORD` o CORS inseguros.

## Objetivo

Endurecer configuracion base, manejo de secretos y documentacion operativa sin agregar features funcionales.

## Usuarios afectados

- Engineering: necesita validacion automatizada de settings.
- DevOps: necesita reglas claras por ambiente.
- Security: necesita evitar secretos por defecto y CORS abierto fuera de desarrollo.
- Future builders: necesitan handoff y acceptance de Fase 1.

## Alcance

- Validar `SECRET_KEY`, `SEED_ADMIN_PASSWORD`, `DATABASE_URL` y `CORS_ORIGINS` fuera de development.
- Mantener development local funcionando.
- Ajustar `docker-compose.yml` con fallbacks locales documentados.
- Crear `docs/SECURITY.md`.
- Agregar tests minimos de configuracion.
- Actualizar planning, docs, metrics y auditoria.

## Fuera de alcance

- Rate limit completo.
- Account lockout.
- Refresh tokens.
- Password reset.
- Alembic.
- Cambios de modelo de datos.
- Cambios UI.
- WhatsApp, S3/R2, mobile, route optimization, autonomous agents.

## Reglas de seguridad

- No guardar secretos reales.
- No imprimir valores secretos en errores.
- `.env` debe permanecer ignorado.
- Los defaults locales solo son permitidos con `APP_ENV=development`.
- `CORS_ORIGINS=*` no se permite fuera de development.

## Variables de entorno

- `APP_ENV`
- `DATABASE_URL`
- `CORS_ORIGINS`
- `OCR_PROVIDER`
- `OPENAI_API_KEY`
- `OPENAI_MODEL`
- `SECRET_KEY`
- `ALGORITHM`
- `ACCESS_TOKEN_EXPIRE_MINUTES`
- `SEED_ADMIN_EMAIL`
- `SEED_ADMIN_PASSWORD`
- `SEED_ADMIN_NAME`

## Riesgos

- Rate limit y lockout quedan pendientes.
- `/uploads` sigue requiriendo politica de acceso de produccion.
- No hay secret scanning en CI.
- No hay migraciones formales.

## Metricas

- `default_secret_detected`
- `secrets_in_repo_count`
- `env_example_completeness`
- `unsafe_production_config_blocked`
- `cors_wildcard_blocked`
- `config_security_tests_passed`

## Criterios de aceptacion

Los criterios verificables estan en `acceptance.md`.
