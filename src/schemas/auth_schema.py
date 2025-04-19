from pydantic import BaseModel, Field   
from typing import Optional


class RefreshBody(BaseModel):
    refresh_token: Optional[str] = Field("Hello")

