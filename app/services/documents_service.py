"""Service operations for project documents."""

from collections.abc import Iterator
from typing import BinaryIO
from urllib.parse import quote

from botocore.exceptions import ClientError
from fastapi import HTTPException, UploadFile
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.core.logger import logger
from app.models.document import Document
from app.repositories.repository import Repository


def _stream_body(body: BinaryIO) -> Iterator[bytes]:
    """Yield storage response chunks and close the body when streaming ends."""
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
) -> StreamingResponse:
    """Stream a document to a member of its project.

    Raises:
        HTTPException: If the document is missing, access is denied, or its
            S3 object does not exist.
    """
    repository = Repository(db)
    document = repository.get_document(document_id)

    if not document:
        logger.info("Document doesn't exist - Document ID=%s", document_id)
        raise HTTPException(
            status_code=404,
            detail="Document not found",
        )

    membership = repository.get_project_member(document.project_id, user_id)

    if not membership:
        logger.info(
            "User doesn't have permission to download document - "
            "Document ID=%s - User ID=%s",
            document.id,
            user_id,
        )
        raise HTTPException(
            status_code=403,
            detail="Only project members can download documents",
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
        "Document downloaded - Document ID=%s - User ID=%s",
        document.id,
        user_id,
    )
    content_disposition = (
        "attachment; filename*=UTF-8''"
        f"{quote(document.filename, safe='')}"
    )
    return StreamingResponse(
        _stream_body(body),
        media_type="application/octet-stream",
        headers={"Content-Disposition": content_disposition},
    )


def update_document(
    db: Session,
    document_id: int,
    file: UploadFile,
    user_id: int,
) -> Document:
    """Replace a document's S3 object and update its database record.

    Raises:
        HTTPException: If the document is missing or access is denied.
    """
    repository = Repository(db)
    document = repository.get_document(document_id)

    if not document:
        logger.info("Document doesn't exist - Document ID=%s", document_id)
        raise HTTPException(
            status_code=404,
            detail="Document not found",
        )

    membership = repository.get_project_member(document.project_id, user_id)

    if not membership:
        logger.info(
            "User doesn't have permission to update document - "
            "Document ID=%s - User ID=%s",
            document.id,
            user_id,
        )
        raise HTTPException(
            status_code=403,
            detail="Only project members can update documents",
        )

    repository.update_document(document, file)

    logger.info(
        "Document updated - Document ID=%s - User ID=%s - Filename=%s",
        document.id,
        user_id,
        file.filename,
    )
    return document


def delete_document(
    db: Session,
    document_id: int,
    user_id: int,
) -> dict[str, str]:
    """Delete a document and its S3 object for an authorized project member.

    Raises:
        HTTPException: If the document is missing or access is denied.
    """
    repository = Repository(db)
    document = repository.get_document(document_id)

    if not document:
        logger.info("Document doesn't exist - Document ID=%s", document_id)
        raise HTTPException(
            status_code=404,
            detail="Document not found",
        )

    membership = repository.get_project_member(document.project_id, user_id)

    if not membership:
        logger.info(
            "User doesn't have permission to delete document - "
            "Document ID=%s - User ID=%s",
            document.id,
            user_id,
        )
        raise HTTPException(
            status_code=403,
            detail="Only project members can delete documents",
        )

    repository.delete_document(document)

    logger.info(
        "Document deleted - Document ID=%s - User ID=%s",
        document.id,
        user_id,
    )
    return {"message": "Document deleted successfully"}
