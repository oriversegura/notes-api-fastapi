from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    """Request model for user login."""

    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    """Response model for authentication tokens."""

    access_token: str
    token_type: str
