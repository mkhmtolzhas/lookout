from pydantic import BaseModel, EmailStr, Field
from .mixins.time_mixin import TimeMixin
from .mixins.id_mixin import IDMixin
from datetime import datetime


class UserBase(BaseModel):
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., min_length=8, description="User's password")

class UserCreate(UserLogin):
    username: str = Field(..., min_length=3, max_length=50, description="User's username")


class UserUpdate(UserCreate):
    subscription_plan: str = Field(None, description="User's subscription plan")
    subscription_expiry: datetime = Field(None, description="User's subscription expiry date")

class UserResponse(UserBase, IDMixin, TimeMixin):
    username: str = Field(..., min_length=3, max_length=50, description="User's username")
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., min_length=8, description="User's password")
    subscription_plan: str = Field(None, description="User's subscription plan")
    subscription_expiry: datetime = Field(None, description="User's subscription expiry date")
