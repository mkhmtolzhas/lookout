from pydantic import BaseModel, Field
from datetime import datetime


class PaymentBase(BaseModel):
    user_id: int = Field(..., description="ID of the user making the payment")
    amount: float = Field(..., description="Amount of the payment")
    payment_status: str = Field(..., description="Status of the payment")

    class Config:
        from_attributes = True


class PaymentCreate(PaymentBase):
    """
    Schema for creating a new payment.
    """
    pass

class PaymentUpdate(PaymentBase):
    """
    Schema for updating an existing payment.
    """
    pass

class PaymentResponse(PaymentBase):
    """
    Schema for the response of a payment.
    """
    id: int = Field(..., description="ID of the payment")
    payment_date: datetime = Field(..., description="Date of the payment")