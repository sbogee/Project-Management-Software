from pydantic import BaseModel

class ProjectCreate(BaseModel):
    name: str
    description: str

class ProjectResponse(BaseModel):
    id: int 
    name: str
    description: str
    owner_id: int
    model_config = {"from_attributes": True}