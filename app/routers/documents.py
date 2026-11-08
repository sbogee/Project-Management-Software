from app.models.user import User
from app.core.dependencies import get_current_user
from app.dependencies import get_db
from app.services.documents_service import (download_document, update_document, delete_document)
from app.schemas.document import DocumentResponse
from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/documents/{document_id}")
def get_document(document_id: int, current_user: User=Depends(get_current_user), db: Session=Depends(get_db)):
    return download_document(db, document_id, current_user.id)


@router.put("/documents/{document_id}", response_model=DocumentResponse)
def update_document_endpoint(document_id: int, file: UploadFile = File(...), current_user: User=Depends(get_current_user), db: Session=Depends(get_db)):
    return update_document(db, document_id, file, current_user.id)


@router.delete("/documents/{document_id}")
def delete_document_endpoint(document_id: int, current_user: User=Depends(get_current_user), db: Session=Depends(get_db)):
    return delete_document(db, document_id, current_user.id)