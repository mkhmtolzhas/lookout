from pydantic import BaseModel, Field


class AuthResponse(BaseModel):
    access_token: str = Field(..., description="Access token for authentication")
    refresh_token: str = Field(..., description="Refresh token for authentication")


class RefreshResponse(BaseModel):
    access_token: str = Field(..., description="New access token for authentication")