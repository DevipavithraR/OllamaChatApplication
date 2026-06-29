from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class MemberBase(BaseModel):
    name: str
    phone_number: str
    email: Optional[str] = None
    gender: Optional[str] = None
    age: Optional[int] = None
    membership_status: str = "ACTIVE"

class MemberCreate(BaseModel):
    name: str
    phone_number: str
    email: Optional[str] = None
    gender: Optional[str] = None
    age: Optional[int] = None
    membership_status: Optional[str] = "ACTIVE"

class MemberUpdate(BaseModel):
    name: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    gender: Optional[str] = None
    age: Optional[int] = None
    membership_status: Optional[str] = None

class MemberResponse(MemberBase):
    member_id: int
    created_at: datetime

    class Config:
        from_attributes = True
