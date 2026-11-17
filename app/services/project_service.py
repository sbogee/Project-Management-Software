"""Business logic for projects and their documents."""

import os
import uuid

from fastapi import HTTPException, UploadFile
from sqlalchemy import case
from sqlalchemy.orm import Session

from app.core.logger import logger
from app.enums.project_role import ProjectRole
from app.models.document import Document
from app.models.project import Project
from app.models.project_member import ProjectMember
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectUpdate


def _projects_with_member_user_ids(db: Session, project_ids: list[int]):
    """Build project response data with member and document identifiers."""
    projects = (
        db.query(Project)
        .filter(Project.id.in_(project_ids))
        .all()
    )
    projects_by_id = {project.id: project for project in projects}

    member_rows = (
        db.query(ProjectMember.project_id, ProjectMember.user_id)
        .filter(ProjectMember.project_id.in_(project_ids))
        .all()
    )
    member_user_ids = {project_id: [] for project_id in project_ids}
    for project_id, user_id in member_rows:
        member_user_ids[project_id].append(user_id)

    document_rows = (
        db.query(Document.project_id, Document.id, Document.filename)
        .filter(Document.project_id.in_(project_ids))
        .all()
    )
    project_documents = {
        project_id: []
        for project_id in project_ids
    }
    for project_id, document_id, filename in document_rows:
        project_documents[project_id].append(
            {
                "id": document_id,
                "filename": filename,
            }
        )

    return [
        {
            "id": project_id,
            "name": projects_by_id[project_id].name,
            "description": projects_by_id[project_id].description,
            "owner_id": projects_by_id[project_id].owner_id,
            "member_user_ids": member_user_ids[project_id],
            "documents": project_documents[project_id],
        }
        for project_id in project_ids
    ]


def create_project(
    db: Session,
    project_data: ProjectCreate,
    owner_id: int,
):
    """Create a project and add its owner as an owner-role member."""
    project = Project(
        name=project_data.name,
        description=project_data.description,
        owner_id=owner_id,
    )
    db.add(project)
    db.commit()
    db.refresh(project)

    owner_member = ProjectMember(
        project_id=project.id,
        user_id=owner_id,
        role=ProjectRole.OWNER,
    )
    db.add(owner_member)
    db.commit()

    logger.info(
        "Project created - " +
        f"Project ID={project.id}"
    )
    return _projects_with_member_user_ids(db, [project.id])[0]


def get_projects(db: Session, user_id):
    """List projects owned by or shared with a user."""
    project_rows = (
        db.query(Project.id)
        .filter(
            (Project.owner_id == user_id)
            | Project.id.in_(
                db.query(ProjectMember.project_id)
                .filter(ProjectMember.user_id == user_id)
            )
        )
        .order_by(case((Project.owner_id == user_id, 0), else_=1))
        .all()
    )

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
    project = (
        db.query(Project)
        .filter(Project.id == project_id)
        .first()
    )

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

    invited_user = (
        db.query(User)
        .filter(User.username == username)
        .first()
    )

    if not invited_user:
        logger.info(
            "User doesn\'t exist - " +
            f"User ID={user_id}"
        )
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    existing_member = (
        db.query(ProjectMember)
        .filter(
            ProjectMember.project_id == project_id,
            ProjectMember.user_id == invited_user.id,
        )
        .first()
    )

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

    member = ProjectMember(
        project_id=project_id,
        user_id=invited_user.id,
        role=ProjectRole.PARTICIPANT,
    )
    db.add(member)
    db.commit()

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
    project = (
        db.query(Project)
        .filter(Project.id == project_id)
        .first()
    )

    if not project:
        logger.info(
            "Project doesn\'t exist - " +
            f"Project ID={project_id}"
        )
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    project_members = (
        db.query(ProjectMember)
        .filter(ProjectMember.project_id == project_id)
        .all()
    )

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
    project = (
        db.query(Project)
        .filter(Project.id == project_id)
        .first()
    )

    if not project:
        logger.info(
            "Project doesn\'t exist - " +
            f"Project ID={project_id}"
        )
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    membership = (
        db.query(ProjectMember)
        .filter(
            ProjectMember.project_id == project_id,
            ProjectMember.user_id == user_id,
        )
        .first()
    )

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

    project.name = project_data.name
    project.description = project_data.description
    db.commit()
    db.refresh(project)

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
    project = (
        db.query(Project)
        .filter(Project.id == project_id)
        .first()
    )

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

    db.query(Document).filter(
        Document.project_id == project_id
    ).delete(synchronize_session=False)
    db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id
    ).delete(synchronize_session=False)
    db.delete(project)
    db.commit()

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
    project = (
        db.query(Project)
        .filter(Project.id == project_id)
        .first()
    )

    if not project:
        logger.info(
            "Project doesn\'t exist - " +
            f"Project ID={project_id}"
        )
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    membership = (
        db.query(ProjectMember)
        .filter(
            ProjectMember.project_id == project_id,
            ProjectMember.user_id == user_id,
        )
        .first()
    )

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

    documents = (
        db.query(Document)
        .filter(Document.project_id == project_id)
        .all()
    )

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

    project = (
        db.query(Project)
        .filter(Project.id == project_id)
        .first()
    )

    if not project:
        logger.info(
            "Project doesn\'t exist - " +
            f"Project ID={project_id}"
        )
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    membership = (
        db.query(ProjectMember)
        .filter(
            ProjectMember.project_id == project_id,
            ProjectMember.user_id == user_id,
        )
        .first()
    )

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

    unique_name = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join("uploads", unique_name)

    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    document = Document(
        filename=file.filename,
        stored_filename=unique_name,
        file_path=file_path,
        project_id=project_id,
        uploaded_by=user_id,
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    logger.info(
        "Document is uploaded successfully - " +
        f"Document filename={file.filename} - " +
        f"Project ID={project_id} - " +
        f"User ID={user_id}"
    )
    return document
