"""Service operations for project documents."""

from urllib.parse import quote

from botocore.exceptions import ClientError
from fastapi import HTTPException, UploadFile
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.core.logger import logger
from app.repositories.repository import Repository


def _stream_body(body):
    try:
        while True:
            chunk = body.read(64 * 1024)
            if not chunk:
                break
            yield chunk
    finally:
        body.close()


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

    try:
        body = repository.get_document_file(document)
    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail="File not found in storage",
        ) from exc
    except ClientError as exc:
        error_code = exc.response.get("Error", {}).get("Code")
        if error_code not in {"NoSuchKey", "NotFound", "404"}:
            raise
        raise HTTPException(
            status_code=404,
            detail="File not found in storage",
        ) from exc

    logger.info(
        "Document downloaded - " +
        f"Document ID={document.id} - " +
        f"User ID={user_id}"
    )
    return StreamingResponse(
        _stream_body(body),
        media_type="application/octet-stream",
        headers={
            "Content-Disposition":
                f"attachment; filename*=UTF-8''{quote(document.filename, safe='')}"
        },
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
