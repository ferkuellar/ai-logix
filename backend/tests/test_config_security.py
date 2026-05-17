import pytest
from pydantic import ValidationError

from app.core.config import Settings


def make_settings(**overrides):
    values = {
        "app_env": "production",
        "database_url": "postgresql://user:password@db:5432/ailogix",
        "cors_origins": "https://app.example.com",
        "secret_key": "a-secure-secret-key-with-at-least-32-chars",
        "seed_admin_password": "SecureAdmin123!",
    }
    values.update(overrides)
    return Settings(_env_file=None, **values)


def test_development_allows_local_defaults():
    settings = Settings(
        _env_file=None,
        app_env="development",
        database_url="postgresql://user:password@db:5432/ailogix",
        secret_key="change-me-in-production",
        seed_admin_password="ChangeMe123!",
        cors_origins="*",
    )

    assert settings.app_env == "development"


def test_production_rejects_default_secret_key():
    with pytest.raises(ValidationError, match="SECRET_KEY must be changed"):
        make_settings(secret_key="change-me-in-production")


def test_production_rejects_short_secret_key():
    with pytest.raises(ValidationError, match="SECRET_KEY must be changed"):
        make_settings(secret_key="short")


def test_production_rejects_default_seed_admin_password():
    with pytest.raises(ValidationError, match="SEED_ADMIN_PASSWORD must be changed"):
        make_settings(seed_admin_password="ChangeMe123!")


def test_production_rejects_wildcard_cors_origins():
    with pytest.raises(ValidationError, match="CORS_ORIGINS cannot include"):
        make_settings(cors_origins="https://app.example.com,*")


def test_production_rejects_missing_database_url():
    with pytest.raises(ValidationError, match="DATABASE_URL is required"):
        make_settings(database_url="")


def test_production_accepts_secure_configuration():
    settings = make_settings()

    assert settings.app_env == "production"
    assert settings.secret_key == "a-secure-secret-key-with-at-least-32-chars"
