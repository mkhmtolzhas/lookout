from datetime import datetime, timedelta
from .base_model import BaseModel
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, text
from .annotations import IDPK, CreatedAt, UpdatedAt


class UserModel(BaseModel):
    __tablename__ = "users"

    id: Mapped[IDPK]
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    subscription_plan: Mapped[str] = mapped_column(String(50), nullable=False, default=text("'free'"))
    subscription_expiry: Mapped[datetime] = mapped_column(
        nullable=False,
        default=lambda: datetime.utcnow() + timedelta(days=30)
    )
    created_at: Mapped[CreatedAt]
    updated_at: Mapped[UpdatedAt]