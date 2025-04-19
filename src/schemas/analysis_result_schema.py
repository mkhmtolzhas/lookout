from pydantic import BaseModel, Field
from .mixins.id_mixin import IDMixin
from .mixins.time_mixin import CreatedAtMixin


class AnalysisResultBase(BaseModel):
    """
    Base schema for analysis result.
    """
    video_id: int = Field(..., description="ID of the video associated with the analysis result")
    prediction: str = Field(..., description="Prediction result of the analysis")
    confidence: float = Field(..., description="Confidence level of the prediction")

class AnalysisResultCreate(AnalysisResultBase):
    """
    Schema for creating a new analysis result entry.
    """
    pass

class AnalysisResultUpdate(AnalysisResultBase):
    """
    Schema for updating an existing analysis result entry.
    """
    pass


class AnalysisResultResponse(AnalysisResultBase, IDMixin, CreatedAtMixin):
    """
    Schema for responding with analysis result entry details.
    """
    pass