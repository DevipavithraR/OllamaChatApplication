from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class IssuedBookBase(BaseModel):
    member_id: int
    book_id: int
    issue_date: date
    due_date: date
    return_date: Optional[date] = None
    status: str = Field("Issued", examples=["Issued", "Returned"])

class IssuedBookCreate(BaseModel):
    member_id: int
    book_id: int
    issue_date: Optional[date] = None
    due_date: date

class IssuedBookUpdate(BaseModel):
    return_date: Optional[date] = None
    status: Optional[str] = None

class IssuedBookResponse(IssuedBookBase):
    issue_id: int
    created_at: datetime
    member_name: Optional[str] = None
    book_title: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
