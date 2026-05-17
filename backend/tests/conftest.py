import os

os.environ["DATABASE_URL"] = "sqlite+pysqlite:///:memory:"
os.environ["OCR_PROVIDER"] = "mock"
os.environ["OPENAI_API_KEY"] = ""
os.environ["OPENAI_MODEL"] = "gpt-4o-mini"
os.environ["SECRET_KEY"] = "test-secret-key"
os.environ["ALGORITHM"] = "HS256"
os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"] = "60"

import pytest
from fastapi.testclient import TestClient

from app.db.base import Base
from app.db.session import SessionLocal, engine
from app.main import app
from app.models.driver import Driver
from app.models.user import User
from app.services.evidence_service import EVIDENCE_DIR
from app.services.auth_service import create_access_token, create_user


def clean_test_evidence_uploads():
    if not EVIDENCE_DIR.exists():
        return

    for item in EVIDENCE_DIR.iterdir():
        if item.name.startswith("."):
            continue
        if item.is_file():
            item.unlink()


@pytest.fixture(autouse=True)
def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    clean_test_evidence_uploads()
    yield
    clean_test_evidence_uploads()


@pytest.fixture()
def anonymous_client():
    return TestClient(app)


def seed_driver(name: str = "Test Driver", phone: str = "5550000000"):
    db = SessionLocal()
    try:
        driver = Driver(name=name, phone=phone, status="ACTIVE")
        db.add(driver)
        db.commit()
        db.refresh(driver)
        return driver
    finally:
        db.close()


def seed_user(email: str, role: str, password: str = "Password123!", driver_id=None):
    db = SessionLocal()
    try:
        return create_user(
            db,
            email=email,
            full_name=f"{role.title()} User",
            password=password,
            role=role,
            driver_id=driver_id,
        )
    finally:
        db.close()


def authenticated_client_for(user):
    client = TestClient(app)
    client.headers.update({"Authorization": f"Bearer {create_access_token(user.id)}"})
    return client


@pytest.fixture()
def admin_user():
    return seed_user("admin@example.com", "ADMIN")


@pytest.fixture()
def supervisor_user():
    return seed_user("supervisor@example.com", "SUPERVISOR")


@pytest.fixture()
def driver_user():
    driver = seed_driver(name="Assigned Driver", phone="5550000001")
    return seed_user("driver@example.com", "DRIVER", driver_id=driver.id)


@pytest.fixture()
def unassigned_driver_user():
    db = SessionLocal()
    try:
        user = User(
            email="unassigned-driver@example.com",
            full_name="Unassigned Driver",
            hashed_password="$2b$12$kno3ra1tg1Q9HSPKRQ9fQuZ8Uaa0QkE5D5hi8gyXk2Pj7GzKyi8aa",
            role="DRIVER",
            is_active=True,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    finally:
        db.close()


@pytest.fixture()
def client(admin_user):
    return authenticated_client_for(admin_user)


@pytest.fixture()
def supervisor_client(supervisor_user):
    return authenticated_client_for(supervisor_user)


@pytest.fixture()
def driver_client(driver_user):
    return authenticated_client_for(driver_user)
