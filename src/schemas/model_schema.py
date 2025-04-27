from pydantic import BaseModel, Field
from typing import Optional, List, Generic, TypeVar, Any


T = TypeVar(name="Schemas", bound=Any)

class ModelSchema(BaseModel, Generic[T]):
    status: str = Field(..., description="Status of the model")
    result: Optional[T] = Field(None, description="Result of the model analysis")
    task_id: Optional[str] = Field(None, description="Task ID for tracking the analysis")


class ModelResultSchema(BaseModel):
    verdict: str = Field(..., description="Final verdict of the analysis")
    real_votes: int = Field(..., description="Number of votes for REAL")
    fake_votes: int = Field(..., description="Number of votes for FAKE")
    total_frames: int = Field(..., description="Total number of frames processed")
    confidence: float = Field(..., description="Confidence level of the analysis")
