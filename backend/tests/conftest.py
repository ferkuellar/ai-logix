import os

os.environ["DATABASE_URL"] = "sqlite+pysqlite:///:memory:"
os.environ["OCR_PROVIDER"] = "mock"
os.environ["OPENAI_API_KEY"] = ""
os.environ["OPENAI_MODEL"] = "gpt-4o-mini"

import pytest
from fastapi.testclient import TestClient

from app.db.base import Base
from app.db.session import engine
from app.main import app


@pytest.fixture(autouse=True)
def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


@pytest.fixture()
def client():
    return TestClient(app)
