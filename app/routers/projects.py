"""Endpoints for project management and project documents."""

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.core.dependencies import get_current_user
from app.schemas.document import DocumentResponse
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectResponse, ProjectUpdate
from app.services.project_service import (
    create_project,
    delete_project,
    get_project_documents,
    get_project_info,
    get_projects,
    invite_user,
    update_project_info,
    upload_project_document,
)

router = APIRouter()


@router.post("/projects", response_model=ProjectResponse)
def create_new_project(
    project: ProjectCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a project owned by the current user."""
    return create_project(db, project, current_user.id)


@router.get("/projects", response_model=list[ProjectResponse])
def list_projects(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List projects available to the current user."""
    return get_projects(db, current_user.id)


@router.post("/projects/{project_id}/invite")
def invite_user_to_project(
    project_id: int,
    user: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Invite a user to a project."""
    return invite_user(db, project_id, user, current_user.id)


@router.get("/projects/{project_id}/info")
def project_info(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Return information about a project."""
    return get_project_info(db, project_id, current_user.id)


@router.put("/projects/{project_id}/info")
def update_project(
    project_id: int,
    project_data: ProjectUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update a project's information."""
    return update_project_info(db, project_id, project_data, current_user.id)


@router.delete("/projects/{project_id}")
def remove_project(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete a project owned by the current user."""
    return delete_project(db, project_id, current_user.id)


@router.get("/projects/{project_id}/documents")
def get_documents(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List documents belonging to a project."""
    return get_project_documents(db, project_id, current_user.id)


@router.post(
    "/projects/{project_id}/documents",
    response_model=DocumentResponse,
)
def upload_documents(
    project_id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Upload a document to a project."""
    return upload_project_document(db, project_id, file, current_user.id)
