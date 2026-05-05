from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "AI Logix"
    app_env: str = "development"
    database_url: str
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"

    class Config:
        env_file = ".env"


settings = Settings()
