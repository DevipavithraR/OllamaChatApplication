from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel, ConfigDict

class StudentCreate(BaseModel):
    name: str
    phone_number: str
    email: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    address: Optional[str] = None
    marks_percentage: Optional[float] = None

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    address: Optional[str] = None
    marks_percentage: Optional[float] = None

class StudentResponse(BaseModel):
    student_id: int
    name: str
    phone_number: str
    email: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    address: Optional[str] = None
    marks_percentage: Optional[float] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
