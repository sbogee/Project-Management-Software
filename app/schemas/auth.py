"""Authentication request and response schemas."""

from pydantic import BaseModel


class TokenResponse(BaseModel):
    """Return an issued bearer token."""

    access_token: str
    token_type: str
