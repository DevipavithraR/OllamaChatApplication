from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class MechanicBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, examples=["Arun Kumar"])
    specialization: str = Field(..., min_length=2, max_length=100, examples=["Engine Repair"])
    experience: int = Field(..., ge=0, examples=[10])
    available_status: str = Field("Available", examples=["Available", "Busy"])

class MechanicCreate(MechanicBase):
    pass

class MechanicUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    specialization: Optional[str] = Field(None, min_length=2, max_length=100)
    experience: Optional[int] = Field(None, ge=0)
    available_status: Optional[str] = Field(None)

class MechanicResponse(MechanicBase):
    mechanic_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
