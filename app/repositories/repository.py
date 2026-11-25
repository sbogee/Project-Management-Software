"""Persistence operations for project, document, and user data."""

import uuid

from botocore.exceptions import ClientError
from fastapi import UploadFile
from sqlalchemy import case
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.logger import logger
from app.core.security import hash_password
from app.core.settings import S3_BUCKET_NAME
from app.enums.project_role import ProjectRole
from app.models.document import Document
from app.models.project import Project
from app.models.project_member import ProjectMember
from app.models.user import User
from app.schemas.project import ProjectCreate
from app.services.s3_service import s3_client


class Repository:
    """Provide database and S3 operations for application services."""

    def __init__(self, db: Session):
        """Bind repository operations to a database session."""
        self.db = db

    def get_project_member_rows(self, project_ids: list[int]):
        """Return projects paired with their member user IDs."""
        return (
            self.db.query(Project, ProjectMember.user_id)
            .outerjoin(ProjectMember, Project.id == ProjectMember.project_id)
            .filter(Project.id.in_(project_ids))
            .all()
        )

    def get_project_document_rows(self, project_ids: list[int]):
        """Return document metadata for the given project IDs."""
        return (
            self.db.query(Document.project_id, Document.id, Document.filename)
            .filter(Document.project_id.in_(project_ids))
            .all()
        )

    def get_project_ids_for_user(self, user_id: int):
        """Return IDs of projects owned by or shared with a user."""
        return (
            self.db.query(Project.id)
            .filter(
                (Project.owner_id == user_id)
                | Project.id.in_(
                    self.db.query(ProjectMember.project_id).filter(
                        ProjectMember.user_id == user_id
                    )
                )
            )
            .order_by(case((Project.owner_id == user_id, 0), else_=1))
            .all()
        )

    def get_project_by_id(self, project_id: int):
        """Return a project by ID, or None if it does not exist."""
        return (
            self.db.query(Project)
            .filter(Project.id == project_id)
            .first()
        )

    def get_user_by_username(self, username: str):
        """Return a user by username, or None if it does not exist."""
        return (
            self.db.query(User)
            .filter(User.username == username)
            .first()
        )

    def get_project_member(self, project_id: int, user_id: int):
        """Return a specific project membership, if one exists."""
        return (
            self.db.query(ProjectMember)
            .filter(
                ProjectMember.project_id == project_id,
                ProjectMember.user_id == user_id,
            )
            .first()
        )

    def get_project_members(self, project_id: int):
        """Return all memberships associated with a project."""
        return (
            self.db.query(ProjectMember)
            .filter(ProjectMember.project_id == project_id)
            .all()
        )

    def get_project_documents(self, project_id: int):
        """Return all document records associated with a project."""
        return (
            self.db.query(Document)
            .filter(Document.project_id == project_id)
            .all()
        )

    def delete_documents_by_project_id(self, project_id: int):
        """Delete a project's S3 objects and document records."""
        documents = self.get_project_documents(project_id)
        for document in documents:
            if document.s3_key:
                s3_client.delete_object(
                    Bucket=S3_BUCKET_NAME,
                    Key=document.s3_key,
                )

        self.db.query(Document).filter(
            Document.project_id == project_id
        ).delete(synchronize_session=False)

    def delete_project_members(self, project_id: int):
        """Delete all membership records associated with a project."""
        self.db.query(ProjectMember).filter(
            ProjectMember.project_id == project_id
        ).delete(synchronize_session=False)

    def create_project(self, project_data: ProjectCreate, owner_id: int):
        """Create a project and add its owner membership."""
        project = Project(
            name=project_data.name,
            description=project_data.description,
            owner_id=owner_id,
        )

        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)

        owner_member = ProjectMember(
            project_id=project.id,
            user_id=owner_id,
            role=ProjectRole.OWNER,
        )
        self.db.add(owner_member)
        self.db.commit()

        return project

    def create_document(
        self,
        file: UploadFile,
        project_id: int,
        user_id: int,
    ):
        """Upload a file to S3 and persist its document record."""
        s3_key = f"projects/{project_id}/{uuid.uuid4()}_{file.filename}"

        file.file.seek(0)
        s3_client.upload_fileobj(file.file, S3_BUCKET_NAME, s3_key)

        document = Document(
            filename=file.filename,
            s3_key=s3_key,
            project_id=project_id,
            uploaded_by=user_id,
        )

        self.db.add(document)
        try:
            self.db.commit()
        except SQLAlchemyError:
            self.db.rollback()
            try:
                s3_client.delete_object(
                    Bucket=S3_BUCKET_NAME,
                    Key=s3_key,
                )
            except ClientError:
                logger.exception("Failed to clean up uploaded S3 object")
            raise
        self.db.refresh(document)

        return document

    def add_project_member(self, project_id: int, user_id: int):
        """Add a participant membership to a project."""
        member = ProjectMember(
            project_id=project_id,
            user_id=user_id,
            role=ProjectRole.PARTICIPANT,
        )
        self.db.add(member)
        self.db.commit()

        return member

    def update_project_info(
        self,
        project: Project,
        project_name: str,
        project_description: str,
    ):
        """Update a project's name and description."""
        project.name = project_name
        project.description = project_description
        self.db.commit()
        self.db.refresh(project)

    def delete_project(self, project: Project):
        """Delete a project and its related records and S3 objects."""
        self.delete_documents_by_project_id(project.id)
        self.delete_project_members(project.id)
        self.db.delete(project)
        self.db.commit()

    def get_document(self, document_id: int):
        """Return a document by ID, or None if it does not exist."""
        return (
            self.db.query(Document)
            .filter(Document.id == document_id)
            .first()
        )

    def update_document(self, document: Document, file: UploadFile):
        """Replace a document's S3 object and update its metadata."""
        old_s3_key = document.s3_key
        new_s3_key = (
            f"projects/{document.project_id}/"
            f"{uuid.uuid4()}_{file.filename}"
        )
        file.file.seek(0)
        s3_client.upload_fileobj(file.file, S3_BUCKET_NAME, new_s3_key)

        document.filename = file.filename
        document.s3_key = new_s3_key

        try:
            self.db.commit()
        except SQLAlchemyError:
            self.db.rollback()
            try:
                s3_client.delete_object(
                    Bucket=S3_BUCKET_NAME,
                    Key=new_s3_key,
                )
            except ClientError:
                logger.exception("Failed to clean up replacement S3 object")
            raise
        self.db.refresh(document)

        if old_s3_key:
            s3_client.delete_object(
                Bucket=S3_BUCKET_NAME,
                Key=old_s3_key,
            )

    def delete_document(self, document: Document):
        """Delete a document's S3 object and database record."""
        if document.s3_key:
            s3_client.delete_object(
                Bucket=S3_BUCKET_NAME,
                Key=document.s3_key,
            )

        self.db.delete(document)
        self.db.commit()

    def get_document_file(self, document: Document):
        """Return the S3 response body for a document."""
        if not document.s3_key:
            raise ValueError(f"Document {document.id} has no S3 object key")
        return s3_client.get_object(
            Bucket=S3_BUCKET_NAME,
            Key=document.s3_key,
        )["Body"]

    def get_user(self, user_name: str):
        """Return a user by username, or None if it does not exist."""
        return (
            self.db.query(User)
            .filter(User.username == user_name)
            .first()
        )

    def create_user(self, user_name: str, password: str):
        """Create a user with a hashed password and persist the record."""
        new_user = User(
            username=user_name,
            password_hash=hash_password(password),
        )
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)

        return new_user
