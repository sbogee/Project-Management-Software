"""Document API response schemas."""

from pydantic import BaseModel


class DocumentResponse(BaseModel):
    """Describe a document returned by the API."""

    id: int
    filename: str
    project_id: int
    model_config = {"from_attributes": True}
