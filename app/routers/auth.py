from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.auth import TokenResponse
from app.services.auth_service import (login_user, create_user)
from app.dependencies import get_db
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.user import UserCreate, UserResponse

router = APIRouter()

@router.post("/auth", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        return create_user(db, user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.post("/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm=Depends(), db: Session = Depends(get_db)):
    token = login_user(db, form_data.username, form_data.password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": token, "token_type": "bearer"}