from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class MemberBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, examples=["Rahul Kumar"])
    phone_number: str = Field(..., min_length=7, max_length=20, examples=["+919876543210"])
    email: Optional[str] = Field(None, examples=["rahul@example.com"])
    membership_type: str = Field("Regular", examples=["Premium"])

class MemberCreate(MemberBase):
    registration_date: Optional[date] = None

class MemberUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    phone_number: Optional[str] = Field(None, min_length=7, max_length=20)
    email: Optional[str] = None
    membership_type: Optional[str] = None

class MemberResponse(MemberBase):
    member_id: int
    registration_date: date
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
