"""Tests for project management and project document endpoints."""

import pytest

from app.enums.project_role import ProjectRole
from app.models.document import Document
from app.models.project_member import ProjectMember
from app.schemas.project import ProjectUpdate
from test_helpers import (
    auth_headers,
    create_project,
    delete_project,
    get_project_documents,
    get_project_info,
    invite_user,
    login_user,
    register_user,
    update_project_info,
    upload_documents,
)


@pytest.fixture
def owner_token(client):
    """Create and authenticate a project owner."""
    assert register_user(client).status_code == 200
    response = login_user(client)
    assert response.status_code == 200
    return response.json()["access_token"]


def create_project_data(client, token, name="Test Project"):
    """Create a project and return its response data."""
    response = create_project(client, token, name)
    assert response.status_code == 200
    return response.json()


def test_create_project(client, db, owner_token):
    """Create a project and verify its owner membership."""
    project = create_project_data(client, owner_token)
    assert project["name"] == "Test Project"

    membership = db.query(ProjectMember).filter_by(
        project_id=project["id"],
        user_id=project["owner_id"],
    ).one()
    assert membership.role == ProjectRole.OWNER


def test_list_users_projects(client, owner_token):
    """List all projects owned by the current user."""
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
    """Allow a project owner to invite another user."""
    assert register_user(client, "other_testuser").status_code == 200
    project = create_project_data(client, owner_token)

    response = invite_user(
        client, owner_token, project["id"], "other_testuser"
    )
    assert response.status_code == 200


def test_invite_existing_member(client, owner_token):
    """Reject inviting a user who is already a project member."""
    assert register_user(client, "other_testuser").status_code == 200
    project = create_project_data(client, owner_token)

    invite_user(client, owner_token, project["id"], "other_testuser")
    response = invite_user(
        client, owner_token, project["id"], "other_testuser"
    )
    assert response.status_code == 400


def test_invite_not_existing_user(client, owner_token):
    """Return 404 when inviting a nonexistent user."""
    project = create_project_data(client, owner_token)

    response = invite_user(
        client, owner_token, project["id"], "other_testuser"
    )
    assert response.status_code == 404


def test_invite_without_right(client, owner_token):
    """Prevent a participant from inviting another user."""
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
    """Return 404 when inviting to a nonexistent project."""
    response = invite_user(client, owner_token, 1, "other_testuser")
    assert response.status_code == 404


def test_get_project_info_about_missing_project(client, owner_token):
    """Return 404 when requesting information for a missing project."""
    assert get_project_info(client, owner_token, 1).status_code == 404


def test_get_project_info_without_right(client, owner_token):
    """Deny project information access to a nonmember."""
    assert register_user(client, "other_testuser").status_code == 200
    create_project_data(client, owner_token)
    member_token = login_user(client, "other_testuser").json()["access_token"]
    assert get_project_info(client, member_token, 1).status_code == 403


def test_get_project_info(client, owner_token):
    """Allow the project owner to request project information."""
    create_project_data(client, owner_token)
    assert get_project_info(client, owner_token, 1).status_code == 200


def test_update_project_info_of_missing_project(client, owner_token):
    """Return 404 when updating a nonexistent project."""
    project_data = ProjectUpdate(
        name="Updated Project",
        description="Updated description"
    )
    response = update_project_info(
        client, owner_token, 1, project_data
    )
    assert response.status_code == 404


def test_update_project_info_without_right(client, owner_token):
    """Deny project updates to a nonmember."""
    assert register_user(client, "other_testuser").status_code == 200
    create_project_data(client, owner_token)
    member_token = login_user(client, "other_testuser").json()["access_token"]
    project_data = ProjectUpdate(
        name="Updated Project",
        description="Updated description"
    )
    response = update_project_info(
        client, member_token, 1, project_data
    )
    assert response.status_code == 403


def test_update_project_info(client, owner_token):
    """Allow the project owner to update project information."""
    create_project_data(client, owner_token)
    project_data = ProjectUpdate(
        name="Updated Project",
        description="Updated description"
    )
    response = update_project_info(
        client, owner_token, 1, project_data
    )
    assert response.status_code == 200


def test_delete_missing_project(client, owner_token):
    """Return 404 when deleting a nonexistent project."""
    assert delete_project(client, owner_token, 1).status_code == 404


def test_delete_project_without_right(client, owner_token):
    """Deny project deletion to a nonowner."""
    assert register_user(client, "other_testuser").status_code == 200
    create_project_data(client, owner_token)
    member_token = login_user(client, "other_testuser").json()["access_token"]
    assert delete_project(client, member_token, 1).status_code == 403


def test_delete_project(client, owner_token):
    """Allow the owner to delete their project."""
    create_project_data(client, owner_token)
    assert delete_project(client, owner_token, 1).status_code == 200


def test_delete_project_with_documents(client, db, owner_token, fake_s3):
    """Delete a project, its document records, and their S3 objects."""
    project = create_project_data(client, owner_token)
    upload_response = upload_documents(
        client,
        owner_token,
        project["id"],
        ("plan.txt", b"project plan", "text/plain"),
    )
    assert upload_response.status_code == 200

    document = db.query(Document).filter_by(
        id=upload_response.json()["id"]
    ).one()
    s3_key = document.s3_key
    bucket = next(iter(fake_s3))[0]
    assert (bucket, s3_key) in fake_s3

    response = delete_project(client, owner_token, project["id"])

    assert response.status_code == 200
    assert db.query(Document).filter_by(project_id=project["id"]).count() == 0
    assert (bucket, s3_key) not in fake_s3


def test_get_project_documents_of_missing_project(client, owner_token):
    """Return 404 when listing documents of a missing project."""
    assert get_project_documents(client, owner_token, 1).status_code == 404


def test_get_project_documents_without_right(client, owner_token):
    """Deny document listing to a nonmember."""
    assert register_user(client, "other_testuser").status_code == 200
    create_project_data(client, owner_token)
    member_token = login_user(client, "other_testuser").json()["access_token"]
    assert get_project_documents(client, member_token, 1).status_code == 403


def test_get_project_documents(client, owner_token):
    """Allow the owner to list project documents."""
    create_project_data(client, owner_token)
    assert get_project_documents(client, owner_token, 1).status_code == 200


def test_upload_project_document_to_missing_project(client, owner_token):
    """Return 404 when uploading to a missing project."""
    response = upload_documents(
        client, owner_token, 1, ("plan.txt", b"project plan", "text/plain")
    )
    assert response.status_code == 404


def test_upload_project_document_without_right(client, owner_token):
    """Deny document uploads to a nonmember."""
    assert register_user(client, "other_testuser").status_code == 200
    create_project_data(client, owner_token)
    member_token = login_user(client, "other_testuser").json()["access_token"]

    response = upload_documents(
        client, member_token, 1, ("plan.txt", b"project plan", "text/plain")
    )
    assert response.status_code == 403


def test_upload_project_document(client, db, owner_token, fake_s3):
    """Allow the owner to upload a project document to S3."""
    create_project_data(client, owner_token)

    response = upload_documents(
        client, owner_token, 1, ("plan.txt", b"project plan", "text/plain")
    )
    assert response.status_code == 200
    assert response.json()["filename"] == "plan.txt"
    assert response.json()["project_id"] == 1

    document = db.query(Document).filter_by(id=response.json()["id"]).one()
    bucket, key = next(iter(fake_s3))
    assert document.s3_key == key
    assert fake_s3[(bucket, key)] == b"project plan"
