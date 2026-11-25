"""User registration and authentication services."""

from sqlalchemy.orm import Session

from app.models.user import User
from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.core.logger import logger
from app.schemas.user import UserCreate
from app.repositories.repository import Repository


def create_user(db: Session, user: UserCreate):
    """Create a user account and persist its password hash.

    Raises:
        ValueError: If the username is already registered.
    """
    repository = Repository(db)
    existing_user = repository.get_user(user.username)

    if existing_user:
        logger.info(
            "Username is already taken - " +
            f"Username={user.username}"
        )
        raise ValueError("User already exists")

    new_user = repository.create_user(user.username, user.password)

    logger.info(
        "Registration successful - " +
        f"Username={user.username}"
    )
    return new_user


def login_user(db: Session, username: str, password: str):
    """Return an access token for valid credentials, or None otherwise."""
    repository = Repository(db)
    existing_user = repository.get_user(username)

    if not existing_user:
        logger.info(
            "User doesn\'t exist - " +
            f"Username={username}"
        )
        return None

    if not verify_password(password, existing_user.password_hash):
        logger.info(
            "Password is incorrect - " +
            f"Username={username}"
        )
        return None

    token = create_access_token(
        {"sub": str(existing_user.id), "login": existing_user.username}
    )

    logger.info(
        "Login successful - " +
        f"Username={username}"
    )
    return token
