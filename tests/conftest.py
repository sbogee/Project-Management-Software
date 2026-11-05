import pytest
from app.db.database import SessionLocal
from sqlalchemy import text


@pytest.fixture(autouse=True)
def clean_database():
    db = SessionLocal()

    db.execute(text(
        "TRUNCATE TABLE "
        "documents, "
        "project_members, "
        "projects, "
        "users "
        "RESTART IDENTITY CASCADE"
    ))

    db.commit()
    db.close()
