from .base_model import BaseModel
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, ForeignKey
from .annotations import IDPK, CreatedAt


class LogsModel(BaseModel):
    __tablename__ = "logs"

    id: Mapped[IDPK]
    user_id: Mapped[Integer] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    action: Mapped[String] = mapped_column(String(255), nullable=False)
    details: Mapped[String] = mapped_column(String(255), nullable=True)
    timestamp: Mapped[CreatedAt]
    