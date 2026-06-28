from datetime import datetime
from typing import Optional
from decimal import Decimal
from pydantic import BaseModel, ConfigDict

class DoctorCreate(BaseModel):
    name: str
    department: str
    specialization: str
    experience: int
    consultation_fee: Decimal
    available_days: str
    available_time: str
    status: Optional[str] = "ACTIVE"

class DoctorUpdate(BaseModel):
    name: Optional[str] = None
    department: Optional[str] = None
    specialization: Optional[str] = None
    experience: Optional[int] = None
    consultation_fee: Optional[Decimal] = None
    available_days: Optional[str] = None
    available_time: Optional[str] = None
    status: Optional[str] = None

class DoctorResponse(BaseModel):
    doctor_id: int
    name: str
    department: str
    specialization: str
    experience: int
    consultation_fee: Decimal
    available_days: str
    available_time: str
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
