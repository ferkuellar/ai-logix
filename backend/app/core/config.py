from pydantic import model_validator
from pydantic_settings import BaseSettings


UNSAFE_SECRET_KEYS = {
    "",
    "change-me-in-production",
    "replace-with-a-long-random-secret",
}
UNSAFE_SEED_ADMIN_PASSWORDS = {
    "",
    "ChangeMe123!",
}


class Settings(BaseSettings):
    app_name: str = "AI Logix"
    app_env: str = "development"
    database_url: str
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"
    ocr_provider: str = "mock"
    openai_api_key: str | None = None
    openai_model: str = "gpt-4o-mini"
    secret_key: str = "change-me-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    seed_admin_email: str = "admin@ailogix.local"
    seed_admin_password: str = "ChangeMe123!"
    seed_admin_name: str = "System Admin"

    @model_validator(mode="after")
    def validate_non_development_security(self):
        if self.app_env.lower() == "development":
            return self

        if not self.database_url:
            raise ValueError(
                "Unsafe production configuration: DATABASE_URL is required for non-development environments."
            )

        if self.secret_key in UNSAFE_SECRET_KEYS or len(self.secret_key) < 32:
            raise ValueError(
                "Unsafe production configuration: SECRET_KEY must be changed for non-development environments."
            )

        if (
            self.seed_admin_password in UNSAFE_SEED_ADMIN_PASSWORDS
            or len(self.seed_admin_password) < 12
        ):
            raise ValueError(
                "Unsafe production configuration: SEED_ADMIN_PASSWORD must be changed for non-development environments."
            )

        cors_origins = [
            origin.strip()
            for origin in self.cors_origins.split(",")
            if origin.strip()
        ]
        if "*" in cors_origins:
            raise ValueError(
                "Unsafe production configuration: CORS_ORIGINS cannot include '*' for non-development environments."
            )

        return self

    class Config:
        env_file = ("../.env", ".env")
        extra = "ignore"


settings = Settings()
