"""Project API request and response schemas."""

from pydantic import BaseModel, Field


class ProjectCreate(BaseModel):
    """Validate project creation data."""

    name: str
    description: str


class ProjectResponse(BaseModel):
    """Represent a project and its related identifiers."""

    id: int
    name: str
    description: str
    owner_id: int
    member_user_ids: list[int]
    documents: list[dict] = Field(default_factory=list)
    model_config = {"from_attributes": True}


class ProjectUpdate(BaseModel):
    """Validate project update data."""

    name: str
    description: str
