from pydantic import BaseModel, Field
from typing import Generic, TypeVar, Any


T = TypeVar(name="Schemas", bound=Any)


class GeneralResponse(BaseModel, Generic[T]):
    """
    General response schema for API responses.
    """
    status: str = Field(..., description="Status of the response")
    message: str = Field(..., description="Message providing additional information about the response")
    data: T = Field(..., description="Data returned in the response, if any")