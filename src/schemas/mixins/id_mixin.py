from pydantic import BaseModel, Field

class IDMixin(BaseModel):
    id: int = Field(..., description="Unique identifier")