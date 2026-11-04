from pydantic import BaseModel

class DocumentResponse(BaseModel):
    id: int
    filename: str
    project_id: int
    model_config = {"from_attributes": True}