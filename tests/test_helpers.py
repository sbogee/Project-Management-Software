PASSWORD = "password123"


def register_user(client, username="testuser", password=PASSWORD):
    return client.post(
        "/auth",
        json={"username": username, "password": password},
    )


def login_user(client, username="testuser", password=PASSWORD):
    return client.post(
        "/login",
        data={"username": username, "password": password},
    )


def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}


def create_project(client, token, name="Test Project"):
    return client.post(
        "/projects",
        headers=auth_headers(token),
        json={"name": name, "description": "Example"},
    )


def invite_user(client, token, project_id, username):
    return client.post(
        f"/projects/{project_id}/invite",
        params={"user": username},
        headers=auth_headers(token),
    )

def get_project_info(client, token, project_id):
    return client.get(
        f"/projects/{project_id}/info",
        headers=auth_headers(token),
    )

def update_project_info(client, token, project_id, project_data):
    return client.put(
        f"/projects/{project_id}/info",
        json=project_data.model_dump(),
        headers=auth_headers(token),
    )

def delete_project(client, token, project_id):
    return client.delete(
        f"/projects/{project_id}",
        headers=auth_headers(token)
    )

def get_project_documents(client, token, project_id):
    return client.get(
        f"/projects/{project_id}/documents",
        headers=auth_headers(token),
    )

def upload_documents(client, token, project_id, file):
    return client.post(
        f"/projects/{project_id}/documents",
        headers=auth_headers(token),
        files={"file": file},
    )


def get_document(client, token, document_id):
    return client.get(
        f"/documents/{document_id}",
        headers=auth_headers(token),
    )


def update_document(client, token, document_id, file):
    return client.put(
        f"/documents/{document_id}",
        headers=auth_headers(token),
        files={"file": file},
    )


def delete_document(client, token, document_id):
    return client.delete(
        f"/documents/{document_id}",
        headers=auth_headers(token),
    )