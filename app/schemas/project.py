from pydantic import BaseModel, Field

class ProjectCreate(BaseModel):
    name: str
    description: str

class ProjectResponse(BaseModel):
    id: int 
    name: str
    description: str
    owner_id: int
    member_user_ids: list[int]
    documents: list[dict] = Field(default_factory=list)
    model_config = {"from_attributes": True}

class ProjectUpdate(BaseModel):
    name: str
    description: str