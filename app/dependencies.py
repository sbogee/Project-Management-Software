"""Shared FastAPI dependencies."""
from app.db.database import SessionLocal


def get_db():
    """Yield a database session and close it after the request."""
    with SessionLocal() as db:
        yield db
