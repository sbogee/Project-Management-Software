from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import (verify_password, create_access_token)
from app.schemas.user import UserCreate
from app.core.security import hash_password


def create_user(db: Session, user: UserCreate):
    existing_user = (db.query(User).filter(User.username == user.username).first())

    if existing_user:
        raise ValueError("User already exists")

    new_user = User(username=user.username, password_hash=hash_password(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def login_user(db: Session, username: str, password: str):
    existing_user = (db.query(User).filter(User.username == username).first())

    if not existing_user:
        return None

    if not verify_password(password, existing_user.password_hash):
        return None

    token = create_access_token({"sub": str(existing_user.id), "login": existing_user.username})

    return token