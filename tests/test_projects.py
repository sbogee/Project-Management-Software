import pytest
from pathlib import Path
from app.db.database import SessionLocal
from app.enums.project_role import ProjectRole
from app.models.document import Document
from app.models.project_member import ProjectMember
from app.schemas.project import ProjectUpdate
from test_helpers import (
    auth_headers,
    create_project,
    invite_user,
    login_user,
    register_user,
    get_project_info,
    update_project_info,
    delete_project,
    get_project_documents,
    upload_documents,
)


@pytest.fixture
def owner_token(client):
    assert register_user(client).status_code == 200
    response = login_user(client)
    assert response.status_code == 200
    return response.json()["access_token"]


def create_project_data(client, token, name="Test Project"):
    response = create_project(client, token, name)
    assert response.status_code == 200
    return response.json()


def test_create_project(client, owner_token):
    project = create_project_data(client, owner_token)
    assert project["name"] == "Test Project"

    with SessionLocal() as db:
        membership = db.query(ProjectMember).filter_by(
            project_id=project["id"],
            user_id=project["owner_id"],
        ).one()
        assert membership.role == ProjectRole.OWNER


def test_list_users_projects(client, owner_token):
    projects = [
        create_project_data(client, owner_token, "Project 1"),
        create_project_data(client, owner_token, "Project 2"),
    ]

    response = client.get("/projects", headers=auth_headers(owner_token))
    assert response.status_code == 200
    assert {project["id"] for project in response.json()} == {
        project["id"] for project in projects
    }


def test_invite_user(client, owner_token):
    assert register_user(client, "other_testuser").status_code == 200
    project = create_project_data(client, owner_token)

    response = invite_user(
        client, owner_token, project["id"], "other_testuser"
    )
    assert response.status_code == 200


def test_invite_existing_member(client, owner_token):
    assert register_user(client, "other_testuser").status_code == 200
    project = create_project_data(client, owner_token)

    invite_user(client, owner_token, project["id"], "other_testuser")
    response = invite_user(
        client, owner_token, project["id"], "other_testuser"
    )
    assert response.status_code == 400


def test_invite_not_existing_user(client, owner_token):
    project = create_project_data(client, owner_token)

    response = invite_user(
        client, owner_token, project["id"], "other_testuser"
    )
    assert response.status_code == 404


def test_invite_without_right(client, owner_token):
    assert register_user(client, "other_testuser").status_code == 200
    assert register_user(client, "other_other_testuser").status_code == 200
    project = create_project_data(client, owner_token)
    assert invite_user(
        client, owner_token, project["id"], "other_testuser"
    ).status_code == 200

    member_token = login_user(client, "other_testuser").json()["access_token"]
    response = invite_user(
        client, member_token, project["id"], "other_other_testuser"
    )
    assert response.status_code == 403


def test_invite_to_missing_project(client, owner_token):
    response = invite_user(client, owner_token, 1, "other_testuser")
    assert response.status_code == 404


def test_get_project_info_about_missing_project(client, owner_token):
    assert get_project_info(client, owner_token, 1).status_code == 404


def test_get_project_info_without_right(client, owner_token):
    assert register_user(client, "other_testuser").status_code == 200
    create_project_data(client, owner_token)
    member_token = login_user(client, "other_testuser").json()["access_token"]
    assert get_project_info(client, member_token, 1).status_code == 403


def test_get_project_info(client, owner_token):
    create_project_data(client, owner_token)
    assert get_project_info(client, owner_token, 1).status_code == 200


def test_update_project_info_of_missing_project(client, owner_token):
    project_data = ProjectUpdate(
        name="Updated Project",
        description="Updated description"
    )
    assert update_project_info(client, owner_token, 1, project_data).status_code == 404


def test_update_project_info_without_right(client, owner_token):
    assert register_user(client, "other_testuser").status_code == 200
    create_project_data(client, owner_token)
    member_token = login_user(client, "other_testuser").json()["access_token"]
    project_data = ProjectUpdate(
        name="Updated Project",
        description="Updated description"
    )
    assert update_project_info(client, member_token, 1, project_data).status_code == 403


def test_update_project_info(client, owner_token):
    create_project_data(client, owner_token)
    project_data = ProjectUpdate(
        name="Updated Project",
        description="Updated description"
    )
    assert update_project_info(client, owner_token, 1, project_data).status_code == 200


def test_delete_missing_project(client, owner_token):
    assert delete_project(client, owner_token, 1).status_code == 404


def test_delete_project_without_right(client, owner_token):
    assert register_user(client, "other_testuser").status_code == 200
    create_project_data(client, owner_token)
    member_token = login_user(client, "other_testuser").json()["access_token"]
    assert delete_project(client, member_token, 1).status_code == 403


def test_delete_project(client, owner_token):
    create_project_data(client, owner_token)
    assert delete_project(client, owner_token, 1).status_code == 200


def test_get_project_documents_of_missing_project(client, owner_token):
    assert get_project_documents(client, owner_token, 1).status_code == 404


def test_get_project_documents_without_right(client, owner_token):
    assert register_user(client, "other_testuser").status_code == 200
    create_project_data(client, owner_token)
    member_token = login_user(client, "other_testuser").json()["access_token"]
    assert get_project_documents(client, member_token, 1).status_code == 403


def test_get_project_documents(client, owner_token):
    create_project_data(client, owner_token)
    assert get_project_documents(client, owner_token, 1).status_code == 200


def test_upload_project_document_to_missing_project(client, owner_token):
    response = upload_documents(
        client, owner_token, 1, ("plan.txt", b"project plan", "text/plain")
    )
    assert response.status_code == 404


def test_upload_project_document_without_right(client, owner_token):
    assert register_user(client, "other_testuser").status_code == 200
    create_project_data(client, owner_token)
    member_token = login_user(client, "other_testuser").json()["access_token"]

    response = upload_documents(
        client, member_token, 1, ("plan.txt", b"project plan", "text/plain")
    )
    assert response.status_code == 403


def test_upload_project_document(client, owner_token):
    create_project_data(client, owner_token)

    response = upload_documents(
        client, owner_token, 1, ("plan.txt", b"project plan", "text/plain")
    )
    assert response.status_code == 200
    assert response.json()["filename"] == "plan.txt"
    assert response.json()["project_id"] == 1

    with SessionLocal() as db:
        document = db.query(Document).filter_by(id=response.json()["id"]).one()
        Path(document.file_path).unlink(missing_ok=True)
