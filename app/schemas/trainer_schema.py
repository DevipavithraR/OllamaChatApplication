from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from decimal import Decimal

class TrainerBase(BaseModel):
    trainer_name: str
    specialization: str
    experience: str
    available_days: str
    available_time: str
    session_fee: Decimal
    status: str = "ACTIVE"

class TrainerCreate(TrainerBase):
    pass

class TrainerUpdate(BaseModel):
    trainer_name: Optional[str] = None
    specialization: Optional[str] = None
    experience: Optional[str] = None
    available_days: Optional[str] = None
    available_time: Optional[str] = None
    session_fee: Optional[Decimal] = None
    status: Optional[str] = None

class TrainerResponse(TrainerBase):
    trainer_id: int
    created_at: datetime

    class Config:
        from_attributes = True
