from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from app.schemas.patient_schema import PatientResponse
from app.schemas.doctor_schema import DoctorResponse

class AppointmentBase(BaseModel):
    appointment_datetime: datetime = Field(..., examples=["2026-07-01T19:00:00"])
    status: str = Field("CONFIRMED", max_length=20, examples=["CONFIRMED"])
    special_notes: Optional[str] = Field(None, max_length=500, examples=["General checkup, cold symptoms"])

class AppointmentCreate(AppointmentBase):
    patient_id: int
    doctor_id: int

class AppointmentCreateWithPatient(AppointmentBase):
    patient_name: str = Field(..., min_length=2, max_length=100, examples=["John Doe"])
    patient_phone: str = Field(..., min_length=7, max_length=20, examples=["+1234567890"])
    patient_email: Optional[str] = Field(None, examples=["john.doe@example.com"])
    patient_gender: Optional[str] = Field(None, examples=["Male"])
    patient_age: Optional[int] = Field(None, examples=[30])
    doctor_name: str = Field(..., min_length=2, max_length=100, examples=["Dr. Priya"])
    department: Optional[str] = Field(None, examples=["Cardiology"])

class AppointmentReschedule(BaseModel):
    appointment_datetime: datetime

class AppointmentUpdate(BaseModel):
    appointment_datetime: Optional[datetime] = None
    status: Optional[str] = None
    special_notes: Optional[str] = None

class AppointmentResponse(AppointmentBase):
    appointment_id: int
    patient_id: int
    doctor_id: int
    created_at: datetime
    patient: Optional[PatientResponse] = None
    doctor: Optional[DoctorResponse] = None

    model_config = ConfigDict(from_attributes=True)
