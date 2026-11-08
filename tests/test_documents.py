from pathlib import Path

import pytest

from app.db.database import SessionLocal
from app.models.document import Document
from test_helpers import (
    create_project,
    delete_document,
    get_document,
    login_user,
    register_user,
    update_document,
    upload_documents,
)


@pytest.fixture
def owner_token(client):
    assert register_user(client).status_code == 200
    response = login_user(client)
    assert response.status_code == 200
    return response.json()["access_token"]


@pytest.fixture
def project_id(client, owner_token):
    response = create_project(client, owner_token)
    assert response.status_code == 200
    return response.json()["id"]


@pytest.fixture
def project_document(client, owner_token, project_id):
    response = upload_documents(
        client, owner_token, project_id,
        ("initial.txt", b"initial content", "text/plain"),
    )
    assert response.status_code == 200
    document = response.json()

    with SessionLocal() as db:
        original_path = db.query(Document).filter_by(id=document["id"]).one().file_path

    yield document

    with SessionLocal() as db:
        current = db.query(Document).filter_by(id=document["id"]).first()
        if current:
            Path(current.file_path).unlink(missing_ok=True)
    Path(original_path).unlink(missing_ok=True)


def test_download_missing_document(client, owner_token):
    assert get_document(client, owner_token, 1).status_code == 404


def test_download_document_without_right(client, project_document):
    assert register_user(client, "other_testuser").status_code == 200
    token = login_user(client, "other_testuser").json()["access_token"]

    response = get_document(client, token, project_document["id"])
    assert response.status_code == 403


def test_download_document(client, owner_token, project_document):
    response = get_document(client, owner_token, project_document["id"])

    assert response.status_code == 200
    assert response.content == b"initial content"


def test_update_missing_document(client, owner_token):
    response = update_document(
        client, owner_token, 1, ("updated.txt", b"updated", "text/plain")
    )
    assert response.status_code == 404


def test_update_document_without_right(client, project_document):
    assert register_user(client, "other_testuser").status_code == 200
    token = login_user(client, "other_testuser").json()["access_token"]

    response = update_document(
        client, token, project_document["id"],
        ("updated.txt", b"updated", "text/plain"),
    )
    assert response.status_code == 403


def test_update_document(client, owner_token, project_document):
    response = update_document(
        client, owner_token, project_document["id"],
        ("updated.txt", b"updated content", "text/plain"),
    )

    assert response.status_code == 200
    assert response.json()["filename"] == "updated.txt"


def test_delete_missing_document(client, owner_token):
    assert delete_document(client, owner_token, 1).status_code == 404


def test_delete_document_without_right(client, project_document):
    assert register_user(client, "other_testuser").status_code == 200
    token = login_user(client, "other_testuser").json()["access_token"]

    response = delete_document(client, token, project_document["id"])
    assert response.status_code == 403


def test_delete_document(client, owner_token, project_document):
    response = delete_document(client, owner_token, project_document["id"])
    assert response.status_code == 200
    assert response.json() == {"message": "Document deleted successfully"}