from pydantic import BaseModel, Field
from typing import Optional, List, Generic, TypeVar, Any


T = TypeVar(name="Schemas", bound=Any)

class ModelSchema(BaseModel, Generic[T]):
    status: str = Field(..., description="Status of the model")
    result: Optional[T] = Field(None, description="Result of the model analysis")
    task_id: Optional[str] = Field(None, description="Task ID for tracking the analysis")


class ModelResultSchema(BaseModel):
    prediction: str = Field(..., description="Prediction result")
    confidence: float = Field(..., description="Confidence level of the prediction")

