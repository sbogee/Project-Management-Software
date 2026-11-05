from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_register_user():
    response = client.post("/auth",
                           json = {"username": "testuser",
                                   "password": "password123"})

    assert response.status_code == 200
    body = response.json()
    assert body["username"] == "testuser"


def test_register_existing_user():
    response = client.post("/auth",
                           json = {"username": "testuser",
                                   "password": "password123"})

    assert response.status_code == 200

    response = client.post("/auth",
                           json = {"username": "testuser",
                                   "password": "password123"})

    assert response.status_code == 400
    assert response.json() == {"detail": "User already exists"}


def test_login_user():
    response = client.post("/auth",
                           json = {"username": "testuser",
                                   "password": "password123"})
    
    assert response.status_code == 200

    response = client.post("/login",
                           data = {"username": "testuser",
                                   "password": "password123"})

    assert response.status_code == 200

    token = response.json()
    assert "access_token" in token


def test_login_non_existing_user():
    response = client.post("/login",
                           data = {"username": "testuser",
                                   "password": "password123"})

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid credentials"}


def test_login_user_with_bad_password():
    response = client.post("/auth",
                           json = {"username": "testuser",
                                   "password": "password123"})
    
    assert response.status_code == 200

    response = client.post("/login",
                           data = {"username": "testuser",
                                   "password": "password"})

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid credentials"}