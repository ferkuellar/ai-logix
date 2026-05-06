from pydantic_settings import BaseSettings


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

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
