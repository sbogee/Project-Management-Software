from sqlalchemy.orm import Session
from app.models.project import Project
from app.models.project_member import ProjectMember
from app.models.document import Document
from fastapi import HTTPException, UploadFile
import uuid
import os
from fastapi.responses import FileResponse

def download_document(
    db: Session,
    document_id: int,
    user_id: int
):
    document = (
        db.query(Document)
        .filter(Document.id == document_id)
        .first()
    )

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    membership = (
        db.query(ProjectMember)
        .filter(
            ProjectMember.project_id == document.project_id,
            ProjectMember.user_id == user_id
        )
        .first()
    )

    if not membership:
        raise HTTPException(
            status_code=403, 
            detail="Only project members can download documents"
        )

    if not os.path.exists(document.file_path):
        raise HTTPException(
            status_code=404,
            detail="File not found on disk"
        )

    return FileResponse(
        path=document.file_path, 
        filename=document.filename, 
        media_type="application/octet-stream"
    )


def update_document(
    db: Session, 
    document_id: int, 
    file: UploadFile,
    user_id: int
):
    document = (
        db.query(Document)
        .filter(Document.id == document_id)
        .first()
    )

    if not document:
        raise HTTPException(
            status_code=404, 
            detail="Document not found"
        )

    membership = (
        db.query(ProjectMember)
        .filter(
            ProjectMember.project_id == document.project_id,
            ProjectMember.user_id == user_id
        )
        .first()
    )

    if not membership:
        raise HTTPException(
            status_code=403, 
            detail="Only project members can update documents"
        )

    if os.path.exists(document.file_path):
        os.remove(document.file_path)

    unique_name = (f"{uuid.uuid4()}_{file.filename}")

    file_path = os.path.join("uploads", unique_name)

    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    document.filename = file.filename
    document.stored_filename = unique_name
    document.file_path = file_path

    db.commit()
    db.refresh(document)

    return document


def delete_document(
    db: Session, 
    document_id: int, 
    user_id: int
):
    document = (
        db.query(Document)
        .filter(Document.id == document_id)
        .first()
    )

    if not document:
        raise HTTPException(
            status_code=404, 
            detail="Document not found"
        )

    membership = (
        db.query(ProjectMember)
        .filter(
            ProjectMember.project_id == document.project_id,
            ProjectMember.user_id == user_id
        )
        .first()
    )

    if not membership:
        raise HTTPException(
            status_code=403, 
            detail="Only project members can delete documents"
        )

    db.delete(document)
    db.commit()

    return {"message": "Document deleted successfully"}
