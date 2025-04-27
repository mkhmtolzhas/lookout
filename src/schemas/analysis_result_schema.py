from pydantic import BaseModel, Field
from .mixins.id_mixin import IDMixin
from typing import Optional
from .mixins.time_mixin import CreatedAtMixin


class AnalysisResultBase(BaseModel):
    """
    Base schema for analysis result.
    """
    video_id: int = Field(..., description="ID of the video associated with the analysis result")
    task_id: str = Field(..., description="ID of the task associated with the analysis result")
    verdict: str = Field(..., description="Final verdict of the analysis")
    real_votes: int = Field(..., description="Number of votes for REAL")
    fake_votes: int = Field(..., description="Number of votes for FAKE")
    total_frames: int = Field(..., description="Total number of frames processed")
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