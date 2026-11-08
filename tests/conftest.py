import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text

from app.db.database import SessionLocal
from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def clean_database():
    db = SessionLocal()

    db.execute(
        text(
            "TRUNCATE TABLE "
            "documents, "
            "project_members, "
            "projects, "
            "users "
            "RESTART IDENTITY CASCADE"
        )
    )

    db.commit()
    db.close()
