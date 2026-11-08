from sqlalchemy import Column, Integer, String, ForeignKey, Enum as SqlEnum
from app.enums.project_role import ProjectRole
from app.db.database import Base

class ProjectMember(Base):
    __tablename__ = "project_members"
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role = Column(SqlEnum(ProjectRole), nullable=False)