"""Business logic for projects and their documents."""
import os
import uuid
from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session
from app.core.logger import logger
from app.schemas.project import ProjectCreate, ProjectUpdate
from app.repositories.repository import Repository


def _projects_with_member_user_ids(db: Session, project_ids: list[int]):
    """Build project response data with member and document identifiers."""
    repository = Repository(db)
    rows = repository.get_project_member_rows(project_ids)

    member_user_ids = {project.id: [] for project, _ in rows}
    for project, user_id in rows:
        if user_id is None and user_id != project.owner_id:
            member_user_ids[project.id].append(user_id)

    document_rows = repository.get_project_document_rows(project_ids)

    project_documents = {project.id: [] for project, _ in rows}
    for project_id, document_id, filename in document_rows:
        project_documents[project_id].append({
            "id": document_id,
            "filename": filename,
        })

    return [
        {
            "id": project.id,
            "name": project.name,
            "description": project.description,
            "owner_id": project.owner_id,
            "member_user_ids": member_user_ids[project.id],
            "documents": project_documents[project.id],
        }
        for project, _ in rows
    ]


def create_project(
    db: Session,
    project_data: ProjectCreate,
    owner_id: int,
):
    """Create a project and add its owner as an owner-role member."""
    repository = Repository(db)
    project = repository.create_project(project_data, owner_id)

    logger.info(
        "Project created - " +
        f"Project ID={project.id}"
    )
    return _projects_with_member_user_ids(db, [project.id])[0]


def get_projects(db: Session, user_id):
    """List projects owned by or shared with a user."""
    repository = Repository(db)
    project_rows = repository.get_project_ids_for_user(user_id)

    project_ids = [project_id for (project_id,) in project_rows]

    logger.info(
        "Projects are listed - " +
        f"User ID={user_id}"
    )
    return _projects_with_member_user_ids(db, project_ids)


def invite_user(
    db: Session,
    project_id: int,
    username: str,
    user_id: int,
):
    """Add a user as a participant when called by the project owner."""
    repository = Repository(db)
    project = repository.get_project_by_id(project_id)

    if not project:
        logger.info(
            "Project doesn\'t exist - " +
            f"Project ID={project_id}"
        )
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    if project.owner_id != user_id:
        logger.info(
            "User doesn\'t have permission to invite others to the project - " +
            f"Project ID={project_id} - " +
            f"User ID={user_id}"
        )
        raise HTTPException(
            status_code=403,
            detail="Only project owner can invite users"
        )

    invited_user = repository.get_user_by_username(username)

    if not invited_user:
        logger.info(
            "User doesn\'t exist - " +
            f"User ID={user_id}"
        )
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    existing_member = repository.get_project_member(project_id, invited_user.id)

    if existing_member:
        logger.info(
            "User is already added to project - " +
            f"Project ID={project_id} - " +
            f"User ID={invited_user.id}"
        )
        raise HTTPException(
            status_code=400,
            detail="User already has access"
        )

    member = repository.add_project_member(project_id, invited_user.id)

    logger.info(
        "User is invited successfully - " +
        f"Project ID={project_id} - " +
        f"User ID={invited_user.id}"
    )
    return {"message": f"{username} invited successfully"}


def get_project_info(
    db: Session,
    project_id: int,
    user_id: int,
):
    """Return project details to an authorized project member."""
    repository = Repository(db)
    project = repository.get_project_by_id(project_id)

    if not project:
        logger.info(
            "Project doesn\'t exist - " +
            f"Project ID={project_id}"
        )
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    project_members = repository.get_project_members(project_id)

    if (
        project.owner_id != user_id
        and user_id not in project_members
    ):
        logger.info(
            "User doesn\'t have permission to get project info - " +
            f"Project ID={project_id} - " +
            f"User ID={user_id}"
        )
        raise HTTPException(
            status_code=403,
            detail="User doesn't have acces to project"
        )

    logger.info(
        "Project info is returned successfully - " +
        f"Project ID={project_id} - " +
        f"User ID={user_id}"
    )
    return _projects_with_member_user_ids(db, [project.id])


def update_project_info(
    db: Session,
    project_id: int,
    project_data: ProjectUpdate,
    user_id: int,
):
    """Update a project's name and description for an authorized member."""
    repository = Repository(db)
    project = repository.get_project_by_id(project_id)

    if not project:
        logger.info(
            "Project doesn\'t exist - " +
            f"Project ID={project_id}"
        )
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    membership = repository.get_project_member(project_id, user_id)

    if not membership and project.owner_id != user_id:
        logger.info(
            "User doesn\'t have permission to update project info - " +
            f"Project ID={project_id} - " +
            f"User ID={user_id}"
        )
        raise HTTPException(
            status_code=403,
            detail="Only project members can update project infos"
        )

    repository.update_project_info(project, project_data.name, project_data.description)

    logger.info(
        "Project info is updated successfully - " +
        f"Project ID={project_id} - " +
        f"User ID={user_id}"
    )    
    return project


def delete_project(
    db: Session,
    project_id: int,
    user_id: int,
):
    """Delete a project and its membership records if called by its owner."""
    repository = Repository(db)
    project = repository.get_project_by_id(project_id)

    if not project:
        logger.info(
            "Project doesn\'t exist - " +
            f"Project ID={project_id}"
        )
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    if project.owner_id != user_id:
        logger.info(
            "User doesn\'t have permission to delete project - " +
            f"Project ID={project_id} - " +
            f"User ID={user_id}"
        )
        raise HTTPException(
            status_code=403,
            detail="Only project owner can delete project"
        )

    repository.delete_project(project)

    logger.info(
        "Project is deleted successfully - " +
        f"Project ID={project_id} - " +
        f"User ID={user_id}"
    )
    return {"message": "Project deleted successfully"}


def get_project_documents(
    db: Session,
    project_id: int,
    user_id: int,
):
    """List project documents for an authorized project member."""
    repository = Repository(db)
    project = repository.get_project_by_id(project_id)

    if not project:
        logger.info(
            "Project doesn\'t exist - " +
            f"Project ID={project_id}"
        )
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    membership = repository.get_project_member(project_id, user_id)

    if not membership and project.owner_id != user_id:
        logger.info(
            "User doesn\'t have permission to get project documents - " +
            f"Project ID={project_id} - " +
            f"User ID={user_id}"
        )
        raise HTTPException(
            status_code=403,
            detail="Only project members can list project documents"
        )

    documents = repository.get_project_documents(project_id)

    logger.info(
        "Project documents are returned successfully - " +
        f"Project ID={project_id} - " +
        f"User ID={user_id}"
    )
    return documents


def upload_project_document(
    db: Session,
    project_id: int,
    file: UploadFile,
    user_id: int,
):
    """Save an uploaded file and create its project document record."""
    os.makedirs("uploads", exist_ok=True)

    repository = Repository(db)
    project = repository.get_project_by_id(project_id)

    if not project:
        logger.info(
            "Project doesn\'t exist - " +
            f"Project ID={project_id}"
        )
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    membership = repository.get_project_member(project_id, user_id)

    if not membership and project.owner_id != user_id:
        logger.info(
            "User doesn\'t have permission to upload project documents - " +
            f"Project ID={project_id} - " +
            f"User ID={user_id}"
        )
        raise HTTPException(
            status_code=403,
            detail="Only project members can upload documents"
        )

    document = repository.create_document(file, project_id, user_id)

    logger.info(
        "Document is uploaded successfully - " +
        f"Document filename={file.filename} - " +
        f"Project ID={project_id} - " +
        f"User ID={user_id}"
    )
    return document
