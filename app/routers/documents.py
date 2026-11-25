"""Endpoints for downloading, updating, and deleting documents."""

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.models.user import User
from app.core.dependencies import get_current_user
from app.dependencies import get_db
from app.schemas.document import DocumentResponse
from app.services.documents_service import (
    delete_document,
    download_document,
    update_document,
)

router = APIRouter()


@router.get("/documents/{document_id}")
def get_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Download a document accessible to the current user."""
    return download_document(db, document_id, current_user.id)


@router.put("/documents/{document_id}", response_model=DocumentResponse)
def update_document_endpoint(
    document_id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Replace a document's file."""
    return update_document(db, document_id, file, current_user.id)


@router.delete("/documents/{document_id}")
def delete_document_endpoint(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete a document accessible to the current user."""
    return delete_document(db, document_id, current_user.id)
