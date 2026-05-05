from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "AI Logix"
    app_env: str = "development"
    database_url: str
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"
    ocr_provider: str = "mock"
    openai_api_key: str | None = None
    openai_model: str = "gpt-4o-mini"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
