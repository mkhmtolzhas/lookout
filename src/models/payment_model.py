from .base_model import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey
from .annotations import UpdatedAt, IDPK

class PaymentModel(BaseModel):
    __tablename__ = "payments"

    id: Mapped[IDPK]
    user_id: Mapped[Integer] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)  # Cascade удаление
    amount: Mapped[Integer] = mapped_column(Integer, nullable=False)
    payment_status: Mapped[String] = mapped_column(String(50), nullable=False)
    payment_date: Mapped[UpdatedAt]
    