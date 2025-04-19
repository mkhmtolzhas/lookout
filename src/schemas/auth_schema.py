from pydantic import BaseModel, Field   


class RefreshBody(BaseModel):
    refresh_token: str = Field(..., description="Refresh token for authentication")

