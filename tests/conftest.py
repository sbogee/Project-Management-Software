"""Shared pytest fixtures for API tests."""

from contextlib import asynccontextmanager

import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db.database import Base
from app.dependencies import get_db


@asynccontextmanager
async def _no_database_lifespan(_app):
    """Skip application startup so tests never initialize the configured database."""
    yield


@pytest.fixture(autouse=True)
def disable_database_startup(monkeypatch):
    """Replace the app's startup lifecycle with a no-op for every test."""
    monkeypatch.setattr(app.router, "lifespan_context", _no_database_lifespan)


engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

@pytest.fixture()
def db():
    """Create the test SQLite schema and yield a session, then clean both up."""
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture()
def client(db):
    """Provide an API client whose database dependency uses the test session."""

    def override_get_db():
        """Yield the test session for each request that needs a database."""
        yield db

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()