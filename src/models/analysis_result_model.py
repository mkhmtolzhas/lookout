from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, ForeignKey, Float
from .base_model import BaseModel
from .annotations import IDPK, CreatedAt


class AnalysisResultModel(BaseModel):
    __tablename__ = "analysis_results"

    id: Mapped[IDPK]
    video_id: Mapped[Integer] = mapped_column(ForeignKey("videos.id", ondelete="CASCADE"), nullable=False)
    task_id: Mapped[String] = mapped_column(String(100), nullable=False)
    prediction: Mapped[String] = mapped_column(String(255), nullable=False)
    confidence: Mapped[Float] = mapped_column(Float,nullable=False)
    created_at: Mapped[CreatedAt]