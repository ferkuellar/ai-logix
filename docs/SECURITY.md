# Security

## Secret Policy

- Never commit `.env`.
- Never commit real API keys, passwords, JWT secrets, database credentials, private URLs, or evidence files.
- Use `.env.example` only as a template.
- Use long random values for production secrets.
- Rotate secrets before any shared dev, staging, or production environment.

## Required Variables

- `APP_ENV`
- `DATABASE_URL`
- `CORS_ORIGINS`
- `SECRET_KEY`
- `ALGORITHM`
- `ACCESS_TOKEN_EXPIRE_MINUTES`
- `SEED_ADMIN_EMAIL`
- `SEED_ADMIN_PASSWORD`
- `SEED_ADMIN_NAME`
- `OCR_PROVIDER`
- `OPENAI_MODEL`

`OPENAI_API_KEY` is required only when an OCR provider uses OpenAI.

## Development-Allowed Values

With `APP_ENV=development`, local defaults are allowed for developer convenience:

- Local PostgreSQL URL.
- Local CORS origins.
- Development seed admin password.
- Placeholder JWT secret.

These values must not be used outside development.

## Production-Prohibited Values

When `APP_ENV != development`, the backend rejects:

- Empty `SECRET_KEY`.
- `SECRET_KEY=change-me-in-production`.
- `SECRET_KEY=replace-with-a-long-random-secret`.
- `SECRET_KEY` shorter than 32 characters.
- Empty `SEED_ADMIN_PASSWORD`.
- `SEED_ADMIN_PASSWORD=ChangeMe123!`.
- `SEED_ADMIN_PASSWORD` shorter than 12 characters.
- Missing `DATABASE_URL`.
- `CORS_ORIGINS=*`.

Error messages identify the unsafe setting but do not print secret values.

## JWT Secret Policy

- `SECRET_KEY` signs JWTs.
- Use a long random secret outside development.
- Rotate if exposed.
- Do not log the value.
- Do not reuse the same value across unrelated environments.

## Seed Admin Policy

- Seed admin is for controlled setup only.
- Default seed password is development-only.
- Non-development environments must provide a strong seed password or disable seed usage by process.
- Change or deactivate seeded accounts after initial provisioning when appropriate.

## CORS Policy

- Development may use localhost origins.
- Non-development must use explicit trusted origins.
- Wildcard `*` is blocked outside development.

## `.env` Handling

- Create local `.env` from `.env.example`.
- Keep `.env` untracked.
- Do not paste real secrets into docs, issue comments, commit messages, or logs.

## Do Not Commit

- `.env`
- API keys
- JWT secrets
- Database passwords
- Evidence uploads
- Database dumps
- Local logs containing credentials
- Python bytecode or build artifacts

## Pending Security Risks

- Login rate limiting is not implemented.
- Account lockout is not implemented.
- Refresh tokens are not implemented.
- Password reset is not implemented.
- Evidence access is not protected for production.
- Secret scanning is not automated in CI/CD.
- Formal migration workflow is not implemented.
