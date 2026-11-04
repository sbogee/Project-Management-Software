from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.schemas.project import ProjectCreate, ProjectResponse
from app.services.project_service import create_project
from app.models.user import User
from app.core.dependencies import get_current_user


router = APIRouter()

@router.post("/projects", response_model=ProjectResponse)
def create_new_project(project: ProjectCreate, current_user: User=Depends(get_current_user), db: Session=Depends(get_db)):
    return create_project(db, project, current_user.id)