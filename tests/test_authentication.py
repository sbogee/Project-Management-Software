"""Tests for user registration and authentication endpoints."""

import pytest

from test_helpers import login_user, register_user


def test_register_user(client):
    """Register a user and check the returned username."""
    response = register_user(client)
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"


def test_register_existing_user(client):
    """Reject registration when the username already exists."""
    register_user(client)
    response = register_user(client)
    assert response.status_code == 400
    assert response.json() == {"detail": "User already exists"}


def test_login_user(client):
    """Issue an access token after successful login."""
    register_user(client)
    response = login_user(client)
    assert response.status_code == 200
    assert "access_token" in response.json()


@pytest.mark.parametrize(
    ("register_first", "password"),
    [(False, "password123"), (True, "wrong-password")],
)
def test_login_rejects_invalid_credentials(client, register_first, password):
    """Reject login for unknown users or incorrect passwords."""
    if register_first:
        register_user(client)
    response = login_user(client, password=password)
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid credentials"}
