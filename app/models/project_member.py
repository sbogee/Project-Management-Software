"""Database model for project membership and roles."""

from sqlalchemy import Column, Enum as SqlEnum, ForeignKey, Integer

from app.enums.project_role import ProjectRole
from app.db.database import Base


class ProjectMember(Base):
    """Associate users with projects and their access roles."""

    __tablename__ = "project_members"
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role = Column(SqlEnum(ProjectRole), nullable=False)
