from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

class PatientCreate(BaseModel):
    name: str
    phone_number: str
    email: Optional[str] = None
    gender: Optional[str] = None
    age: Optional[int] = None

class PatientUpdate(BaseModel):
    name: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    gender: Optional[str] = None
    age: Optional[int] = None

class PatientResponse(BaseModel):
    patient_id: int
    name: str
    phone_number: str
    email: Optional[str] = None
    gender: Optional[str] = None
    age: Optional[int] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
