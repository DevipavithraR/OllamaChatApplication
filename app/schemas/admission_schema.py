from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel, ConfigDict
from app.schemas.student_schema import StudentResponse
from app.schemas.course_schema import CourseResponse

class AdmissionCreate(BaseModel):
    student_id: int
    course_id: int
    application_date: date
    status: Optional[str] = "Pending Verification"
    remarks: Optional[str] = None

class AdmissionCreateWithStudent(BaseModel):
    student_name: str
    student_phone: str
    student_email: Optional[str] = None
    student_dob: Optional[date] = None
    student_gender: Optional[str] = None
    student_address: Optional[str] = None
    marks_percentage: Optional[float] = None
    course_name: str
    application_date: date
    remarks: Optional[str] = None

class AdmissionUpdate(BaseModel):
    status: Optional[str] = None
    remarks: Optional[str] = None

class AdmissionResponse(BaseModel):
    admission_id: int
    student_id: int
    course_id: int
    application_date: date
    status: str
    remarks: Optional[str] = None
    created_at: datetime
    student: Optional[StudentResponse] = None
    course: Optional[CourseResponse] = None

    model_config = ConfigDict(from_attributes=True)
