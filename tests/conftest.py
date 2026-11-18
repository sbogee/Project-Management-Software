"""Shared pytest fixtures for API tests."""

from contextlib import asynccontextmanager
from io import BytesIO
import os

import pytest
from botocore.exceptions import ClientError
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Keep tests independent of developer and production database credentials.
os.environ.setdefault("DATABASE_URL", "sqlite://")
os.environ.setdefault("SECRET_KEY", "test-only-secret-key")
os.environ.setdefault("AWS_ACCESS_KEY_ID", "test-access-key")
os.environ.setdefault("AWS_SECRET_ACCESS_KEY", "test-secret-key")
os.environ.setdefault("AWS_REGION", "us-east-1")
os.environ.setdefault("S3_BUCKET_NAME", "test-bucket")

from app.main import app  # noqa: E402
from app.db.database import Base  # noqa: E402
from app.dependencies import get_db  # noqa: E402


@asynccontextmanager
async def _no_database_lifespan(_app):
    """Skip startup so tests do not initialize the configured database."""
    yield


@pytest.fixture(autouse=True)
def disable_database_startup(monkeypatch):
    """Replace the app's startup lifecycle with a no-op for every test."""
    monkeypatch.setattr(app.router, "lifespan_context", _no_database_lifespan)


@pytest.fixture(autouse=True)
def fake_s3(monkeypatch):
    """Provide isolated in-memory S3 storage for each test."""
    from app.services.s3_service import s3_client

    objects = {}

    def upload_fileobj(fileobj, bucket, key):
        """Store an uploaded object in the in-memory test bucket."""
        objects[(bucket, key)] = fileobj.read()

    def get_object(Bucket, Key):
        """Return an object or raise an S3-style missing-key error."""
        try:
            content = objects[(Bucket, Key)]
        except KeyError as exc:
            raise ClientError(
                {"Error": {"Code": "NoSuchKey", "Message": "Not found"}},
                "GetObject",
            ) from exc
        return {"Body": BytesIO(content)}

    def delete_object(Bucket, Key):
        """Remove an object from the in-memory test bucket."""
        objects.pop((Bucket, Key), None)
        return {}

    monkeypatch.setattr(s3_client, "upload_fileobj", upload_fileobj)
    monkeypatch.setattr(s3_client, "get_object", get_object)
    monkeypatch.setattr(s3_client, "delete_object", delete_object)
    return objects


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
    """Create the test schema, yield a session, and then clean up."""
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client(db):
    """Provide an API client with the test database dependency."""

    def override_get_db():
        """Yield the test session for each request that needs a database."""
        yield db

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
