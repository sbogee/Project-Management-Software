from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.schemas.project import ProjectCreate, ProjectResponse, ProjectUpdate
from app.services.project_service import (create_project, get_projects, invite_user, get_project_info, update_project_info, delete_project)
from app.models.user import User
from app.core.dependencies import get_current_user
from typing import List

router = APIRouter()


@router.post("/projects", response_model=ProjectResponse)
def create_new_project(project: ProjectCreate, current_user: User=Depends(get_current_user), db: Session=Depends(get_db)):
    return create_project(db, project, current_user.id)


@router.get("/projects", response_model=list[ProjectResponse])
def list_projects(db: Session=Depends(get_db), current_user: User=Depends(get_current_user)):
    return get_projects(db, current_user.id)


@router.post("/projects/{project_id}/invite")
def invite_user_to_project(project_id: int, user: str, current_user: User=Depends(get_current_user), db: Session=Depends(get_db)):
    return invite_user(db, project_id, user, current_user.id)


@router.get("/projects/{project_id}/info")
def project_info(project_id: int, current_user: User=Depends(get_current_user), db: Session=Depends(get_db)):
    return get_project_info(db, project_id, current_user.id)


@router.put("/projects/{project_id}/info")
def update_project(project_id: int, project_data: ProjectUpdate, current_user: User=Depends(get_current_user), db: Session=Depends(get_db)):
    return update_project_info(db, project_id, project_data, current_user.id)


@router.delete("/projects/{project_id}")
def remove_project(project_id: int, current_user: User=Depends(get_current_user), db: Session=Depends(get_db)):
    return delete_project(db, project_id, current_user.id)