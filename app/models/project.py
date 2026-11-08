"""Database model for projects."""

from sqlalchemy import Column, Integer, String, Text

from app.db.database import Base


class Project(Base):
    """Persist project details and ownership."""

    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    owner_id = Column(Integer, nullable=False)
