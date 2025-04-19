from pydantic import BaseModel, Field
from datetime import datetime


class TimeMixin(BaseModel):
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")


class CreatedAtMixin(BaseModel):
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")