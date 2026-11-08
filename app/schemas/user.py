"""User API request and response schemas."""

from pydantic import BaseModel


class UserCreate(BaseModel):
    """Validate user registration data."""

    username: str
    password: str


class UserResponse(BaseModel):
    """Represent public user information."""

    id: int
    username: str
    model_config = {"from_attributes": True}
