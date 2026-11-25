"""Reusable helpers for API endpoint tests."""

PASSWORD = "password123"


def register_user(client, username="testuser", password=PASSWORD):
    """Register a user with the test API."""
    return client.post(
        "/auth",
        json={"username": username, "password": password},
    )


def login_user(client, username="testuser", password=PASSWORD):
    """Log in a user and return the API response."""
    return client.post(
        "/login",
        data={"username": username, "password": password},
    )


def auth_headers(token):
    """Build authorization headers for a bearer token."""
    return {"Authorization": f"Bearer {token}"}


def create_project(client, token, name="Test Project"):
    """Create a project and return the API response."""
    return client.post(
        "/projects",
        headers=auth_headers(token),
        json={"name": name, "description": "Example"},
    )


def invite_user(client, token, project_id, username):
    """Invite a user to a project."""
    return client.post(
        f"/projects/{project_id}/invite",
        params={"user": username},
        headers=auth_headers(token),
    )


def get_project_info(client, token, project_id):
    """Fetch project information."""
    return client.get(
        f"/projects/{project_id}/info",
        headers=auth_headers(token),
    )


def update_project_info(client, token, project_id, project_data):
    """Update a project's information."""
    return client.put(
        f"/projects/{project_id}/info",
        json=project_data.model_dump(),
        headers=auth_headers(token),
    )


def delete_project(client, token, project_id):
    """Delete a project."""
    return client.delete(
        f"/projects/{project_id}",
        headers=auth_headers(token),
    )


def get_project_documents(client, token, project_id):
    """List a project's documents."""
    return client.get(
        f"/projects/{project_id}/documents",
        headers=auth_headers(token),
    )


def upload_documents(client, token, project_id, file):
    """Upload a file to a project."""
    return client.post(
        f"/projects/{project_id}/documents",
        headers=auth_headers(token),
        files={"file": file},
    )


def get_document(client, token, document_id):
    """Download a document."""
    return client.get(
        f"/documents/{document_id}",
        headers=auth_headers(token),
    )


def update_document(client, token, document_id, file):
    """Replace a document's file."""
    return client.put(
        f"/documents/{document_id}",
        headers=auth_headers(token),
        files={"file": file},
    )


def delete_document(client, token, document_id):
    """Delete a document."""
    return client.delete(
        f"/documents/{document_id}",
        headers=auth_headers(token),
    )
