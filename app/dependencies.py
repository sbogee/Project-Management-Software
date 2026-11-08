"""Shared FastAPI dependencies."""

from sqlalchemy.orm import Session

from app.db.database import SessionLocal


def get_db():
    """Yield a database session and close it after the request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
