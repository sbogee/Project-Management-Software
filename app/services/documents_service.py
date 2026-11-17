"""Service operations for project documents."""

import os
import uuid

from fastapi import HTTPException, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.core.logger import logger
from app.models.document import Document
from app.models.project_member import ProjectMember


def download_document(
    db: Session,
    document_id: int,
    user_id: int,
):
    """Return a document file if the user belongs to its project.
    Raises:
        HTTPException: If the document or file is missing, or access is denied.
    """
    document = (
        db.query(Document)
        .filter(Document.id == document_id)
        .first()
    )

    if not document:
        logger.info(
            "Document doesn\'t exist - " +
            f"Document ID={document_id}"
        )
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    membership = (
        db.query(ProjectMember)
        .filter(
            ProjectMember.project_id == document.project_id,
            ProjectMember.user_id == user_id,
        )
        .first()
    )

    if not membership:
        logger.info(
            "User doesn\'t have permission to download document - " +
            f"Document ID={document.id} - " +
            f"User ID={user_id}"
        )
        raise HTTPException(
            status_code=403,
            detail="Only project members can download documents"
        )

    if not os.path.exists(document.file_path):
        logger.info(
            "Document doesn\'t exist at filepath - " +
            f"Document ID={document.id} - " + 
            f"Filepath={document.file_path}"
        )
        raise HTTPException(
            status_code=404,
            detail="File not found on disk"
        )

    logger.info(
        "Document downloaded - " +
        f"Document ID={document.id} - " +
        f"User ID={user_id}"
    )
    return FileResponse(
        path=document.file_path,
        filename=document.filename,
        media_type="application/octet-stream",
    )


def update_document(
    db: Session,
    document_id: int,
    file: UploadFile,
    user_id: int,
):
    """Replace a document's stored file and update its database record.
    Raises:
        HTTPException: If the document is missing or access is denied.
    """
    document = (
        db.query(Document)
        .filter(Document.id == document_id)
        .first()
    )

    if not document:
        logger.info(
            "Document doesn\'t exist - " +
            f"Document ID={document_id}"
        )
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    membership = (
        db.query(ProjectMember)
        .filter(
            ProjectMember.project_id == document.project_id,
            ProjectMember.user_id == user_id,
        )
        .first()
    )

    if not membership:
        logger.info(
            "User doesn\'t have permission to update document - " +
            f"Document ID={document.id} - " +
            f"User ID={user_id}"
        )
        raise HTTPException(
            status_code=403,
            detail="Only project members can update documents"
        )

    if os.path.exists(document.file_path):
        os.remove(document.file_path)

    unique_name = f"{uuid.uuid4()}_{file.filename}"

    file_path = os.path.join("uploads", unique_name)

    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    document.filename = file.filename
    document.stored_filename = unique_name
    document.file_path = file_path

    db.commit()
    db.refresh(document)

    logger.info(
        "Document updated - " +
        f"Document ID={document.id} - " +
        f"User ID={user_id} - " +
        f"Filename={file.filename}"
    )
    return document


def delete_document(
    db: Session,
    document_id: int,
    user_id: int,
):
    """Delete a document record if the user belongs to its project.
    Raises:
        HTTPException: If the document is missing or access is denied.
    """
    document = (
        db.query(Document)
        .filter(Document.id == document_id)
        .first()
    )

    if not document:
        logger.info(
            "Document doesn\'t exist - " +
            f"Document ID={document_id}"
        )
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    membership = (
        db.query(ProjectMember)
        .filter(
            ProjectMember.project_id == document.project_id,
            ProjectMember.user_id == user_id,
        )
        .first()
    )

    if not membership:
        logger.info(
            "User doesn\'t have permission to delete document - " +
            f"Document ID={document.id} - " +
            f"User ID={user_id}"
        )
        raise HTTPException(
            status_code=403,
            detail="Only project members can delete documents"
        )

    if os.path.exists(document.file_path):
        os.remove(document.file_path)

    db.delete(document)
    db.commit()

    logger.info(
        "Document deleted - " +
        f"Document ID={document.id} - " +
        f"User ID={user_id}"
    )
    return {"message": "Document deleted successfully"}
