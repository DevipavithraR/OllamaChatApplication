from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

class CourseCreate(BaseModel):
    course_name: str
    department_id: int
    duration: str
    total_seats: int
    available_seats: int
    fees: float
    eligibility: str
    description: Optional[str] = None

class CourseUpdate(BaseModel):
    course_name: Optional[str] = None
    department_id: Optional[int] = None
    duration: Optional[str] = None
    total_seats: Optional[int] = None
    available_seats: Optional[int] = None
    fees: Optional[float] = None
    eligibility: Optional[str] = None
    description: Optional[str] = None

class CourseResponse(BaseModel):
    course_id: int
    course_name: str
    department_id: int
    duration: str
    total_seats: int
    available_seats: int
    fees: float
    eligibility: str
    description: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
