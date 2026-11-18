"""Service operations for project documents."""

import os
import uuid

from fastapi import HTTPException, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.core.logger import logger
from app.repositories.repository import Repository


def download_document(
    db: Session,
    document_id: int,
    user_id: int,
):
    """Return a document file if the user belongs to its project.
    Raises:
        HTTPException: If the document or file is missing, or access is denied.
    """
    repository = Repository(db)
    document = repository.get_document(document_id)

    if not document:
        logger.info(
            "Document doesn\'t exist - " +
            f"Document ID={document_id}"
        )
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    membership = repository.get_project_member(document.project_id, user_id)

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
    repository = Repository(db)
    document = repository.get_document(document_id)

    if not document:
        logger.info(
            "Document doesn\'t exist - " +
            f"Document ID={document_id}"
        )
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    membership = repository.get_project_member(document.project_id, user_id)

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

    repository.update_document(document, file)

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
    repository = Repository(db)
    document = repository.get_document(document_id)

    if not document:
        logger.info(
            "Document doesn\'t exist - " +
            f"Document ID={document_id}"
        )
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    membership = repository.get_project_member(document.project_id, user_id)

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

    repository.delete_document(document)

    logger.info(
        "Document deleted - " +
        f"Document ID={document.id} - " +
        f"User ID={user_id}"
    )
    return {"message": "Document deleted successfully"}
