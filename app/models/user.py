"""Database model for user accounts."""

from sqlalchemy import Column, Integer, String

from app.db.database import Base


class User(Base):
    """Persist a user's unique username and password hash."""

    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
