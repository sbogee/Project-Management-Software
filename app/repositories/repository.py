from sqlalchemy.orm import Session
from app.models.project import Project
from app.models.project_member import ProjectMember
from app.models.document import Document
from app.models.user import User
from sqlalchemy import case
from app.schemas.project import ProjectCreate
from app.enums.project_role import ProjectRole
from fastapi import UploadFile
import os
import uuid
from app.core.security import hash_password

class Repository:
    def __init__(self, db: Session):
        self.db = db


    def get_project_member_rows(self, project_ids: list[int]):
        return (
            self.db.query(Project, ProjectMember.user_id)
            .outerjoin(ProjectMember, Project.id == ProjectMember.project_id)
            .filter(Project.id.in_(project_ids))
            .all()
        )


    def get_project_document_rows(self, project_ids: list[int]):
        return (
            self.db.query(Document.project_id, Document.id, Document.filename)
            .filter(Document.project_id.in_(project_ids))
            .all()
        )


    def get_project_ids_for_user(self, user_id: int):
        return (
            self.db.query(Project.id)
            .filter((Project.owner_id == user_id)
                    | Project.id.in_(self.db.query(ProjectMember.project_id)
                    .filter(ProjectMember.user_id == user_id)))
            .order_by(case((Project.owner_id == user_id, 0), else_=1))
            .all()
        )


    def get_project_by_id(self, project_id: int):
        return (
            self.db.query(Project)
            .filter(Project.id == project_id)
            .first()
        )


    def get_user_by_username(self, username: str):
        return (
            self.db.query(User)
            .filter(User.username == username)
            .first()
        )


    def get_project_member(self, project_id: int, user_id: int):
        return (
            self.db.query(ProjectMember)
            .filter(
                ProjectMember.project_id == project_id,
                ProjectMember.user_id == user_id,
            )
            .first()
        )


    def get_project_members(self, project_id: int):
        return (
            self.db.query(ProjectMember)
            .filter(ProjectMember.project_id == project_id)
            .all()
        )


    def get_project_documents(self, project_id: int):
        return (
            self.db.query(Document)
            .filter(Document.project_id == project_id)
            .all()
        )


    def delete_documents_by_project_id(self, project_id: int):
        self.db.query(Document).filter(
            Document.project_id == project_id
            ).delete(synchronize_session=False)


    def delete_project_members(self, project_id: int):
        self.db.query(ProjectMember).filter(
            ProjectMember.project_id == project_id
            ).delete(synchronize_session=False)


    def create_project(self, project_data: ProjectCreate, owner_id: int):
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


    def create_document(self, file: UploadFile, project_id: int, user_id: int):
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

        self.db.add(document)
        self.db.commit()
        self.db.refresh(document)

        return document


    def add_project_member(self, project_id: int, user_id: int):
        member = ProjectMember(
            project_id=project_id,
            user_id=user_id,
            role=ProjectRole.PARTICIPANT,
        )
        self.db.add(member)
        self.db.commit()

        return member


    def update_project_info(self, project: Project, project_name: str, project_description: str):
        project.name = project_name
        project.description = project_description
        self.db.commit()
        self.db.refresh(project)


    def delete_project(self, project: Project):
        self.delete_documents_by_project_id(project.id)
        self.delete_project_members(project.id)
        self.db.delete(project)
        self.db.commit()


    def get_document(self, document_id: int):
        return (
            self.db.query(Document)
            .filter(Document.id == document_id)
            .first()
        )


    def update_document(self, document: Document, file: UploadFile):
        if os.path.exists(document.file_path):
            os.remove(document.file_path)

        unique_name = f"{uuid.uuid4()}_{file.filename}"

        file_path = os.path.join("uploads", unique_name)

        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())

        document.filename = file.filename
        document.stored_filename = unique_name
        document.file_path = file_path

        self.db.commit()
        self.db.refresh(document)


    def delete_document(self, document: Document):
        if os.path.exists(document.file_path):
            os.remove(document.file_path)
    
        self.db.delete(document)
        self.db.commit()


    def get_user(self, user_name: str):
        return (
            self.db.query(User)
            .filter(User.username == user_name)
            .first()
        )


    def create_user(self, user_name, password):
        new_user = User(
            username=user_name,
            password_hash=hash_password(password),
        )
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)

        return new_user

    
    