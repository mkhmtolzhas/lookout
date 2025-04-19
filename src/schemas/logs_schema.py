from pydantic import BaseModel, Field
from datetime import datetime
from .mixins.id_mixin import IDMixin
from typing import Optional


class LogsBase(BaseModel):
    """
    Base schema for logs.
    """
    user_id: int = Field(..., description="ID of the user who performed the action")
    action: str = Field(..., description="Action performed by the user")
    details: Optional[str] = Field(None, description="Additional details about the action")

    class Config:
        from_attributes = True


class LogsCreate(LogsBase):
    """
    Schema for creating a new log entry.
    """
    pass


class LogsUpdate(LogsCreate):
    """
    Schema for updating an existing log entry.
    """
    pass


class LogsResponse(LogsCreate, IDMixin):
    """
    Schema for responding with log entry details.
    """
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Timestamp of the action")