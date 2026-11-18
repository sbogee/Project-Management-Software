"""Database model for uploaded project documents."""

from sqlalchemy import Column, ForeignKey, Integer, String

from app.db.database import Base


class Document(Base):
    """Persist metadata and storage location for an uploaded document."""

    __tablename__ = "documents"
    id = Column(Integer, primary_key=True)
    filename = Column(String(255), nullable=False)
    s3_key = Column(String(500), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    uploaded_by = Column(Integer, ForeignKey("users.id"), nullable=False)
