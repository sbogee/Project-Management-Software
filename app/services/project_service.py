from sqlalchemy.orm import Session
from sqlalchemy import case
from app.models.user import User
from app.models.project import Project
from app.models.project_member import ProjectMember
from app.schemas.project import ProjectCreate, ProjectUpdate
from fastapi import HTTPException


def _projects_with_member_user_ids(db: Session, projects: list[Project]):
    project_ids = [project.id for project in projects]
    member_rows = (
        db.query(ProjectMember.project_id, ProjectMember.user_id)
        .filter(ProjectMember.project_id.in_(project_ids))
        .all()
    )
    member_user_ids = {project_id: [] for project_id in project_ids}
    for project_id, user_id in member_rows:
        member_user_ids[project_id].append(user_id)

    return [
        {
            "id": project.id,
            "name": project.name,
            "description": project.description,
            "owner_id": project.owner_id,
            "member_user_ids": member_user_ids[project.id],
            "documents": [],
        }
        for project in projects
    ]


def create_project(db: Session, project_data: ProjectCreate, owner_id: int):
    project = Project(name=project_data.name, description=project_data.description, owner_id=owner_id)
    db.add(project)
    db.commit()
    db.refresh(project)

    owner_member = ProjectMember(project_id=project.id, user_id=owner_id, role="OWNER")
    db.add(owner_member)
    db.commit()

    return _projects_with_member_user_ids(db, [project])[0]


def get_projects(db: Session, user_id):
    projects = (db.query(Project)
                .filter((Project.owner_id == user_id) | Project.id.in_(
                        db.query(ProjectMember.project_id)
                        .filter(ProjectMember.user_id == user_id)
                    )
                )
                .order_by(case((Project.owner_id == user_id, 0), else_=1))
                .all())
    return _projects_with_member_user_ids(db, projects)


def invite_user(
    db: Session, 
    project_id: int, 
    username: str, 
    user_id: int
):
    project = (
        db.query(Project)
        .filter(Project.id == project_id)
        .first()
    )

    if not project:
        raise HTTPException(
            status_code=404, 
            detail="Project not found"
        )

    if project.owner_id != user_id:
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
        raise HTTPException(
            status_code=404, 
            detail="User not found"
        )

    existing_member = (
        db.query(ProjectMember)
        .filter(ProjectMember.project_id == project_id, 
                ProjectMember.user_id == invited_user.id)
        .first()
    )

    if existing_member:
        raise HTTPException(
            status_code=400, 
            detail="User already has access"
        )

    member = ProjectMember(
        project_id=project_id,
        user_id=invited_user.id,
        role="PARTICIPANT",
    )
    db.add(member)
    db.commit()

    return {"message": f"{username} invited successfully"}


def get_project_info(
    db: Session, 
    project_id: int, 
    user_id: int
):
    project = (
        db.query(Project)
        .filter(Project.id == project_id)
        .first()
    )

    if not project:
        raise HTTPException(
            status_code=404, 
            detail="Project not found"
        )
     
    project_members = (
        db.query(ProjectMember)
        .filter(ProjectMember.project_id == project_id)
        .all()
    )

    if (project.owner_id != user_id 
        and user_id not in project_members):
        raise HTTPException(
            status_code=403, 
            detail="User doesn't have acces to project"
        )

    return project.description


def update_project_info(
    db: Session, 
    project_id: int, 
    project_data: ProjectUpdate,
    user_id: int
):
    project = (
        db.query(Project)
        .filter(Project.id == project_id)
        .first()
    )

    if not project:
        raise HTTPException(
            status_code=404, 
            detail="Project not found"
        )

    membership = (
        db.query(ProjectMember)
        .filter(
            ProjectMember.project_id == project_id,
            ProjectMember.user_id == user_id
        )
        .first()
    )

    if not membership and project.owner_id != user_id:
        raise HTTPException(
            status_code=403, 
            detail="Only project members can update project infos"
        )

    project.name = project_data.name
    project.description = project_data.description
    db.commit()
    db.refresh(project)

    return project


def delete_project(
    db: Session, 
    project_id: int, 
    user_id: int
):
    project = (
        db.query(Project)
        .filter(Project.id == project_id)
        .first()
    )

    if not project:
        raise HTTPException(
            status_code=404, 
            detail="Project not found"
        )

    if project.owner_id != user_id:
        raise HTTPException(
            status_code=403, 
            detail="Only project owner can update project infos"
        )

    db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id
    ).delete()
    db.delete(project)
    db.commit()

    return {"message": "Project deleted successfully"}

