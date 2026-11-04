from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import (verify_password, create_access_token)

def login_user(db: Session, username: str, password: str):
    existing_user = (db.query(User).filter(User.username == username).first())

    if not existing_user:
        return None

    if not verify_password(password, existing_user.password_hash):
        return None

    token = create_access_token({"sub": str(existing_user.id), "login": existing_user.username})

    return token