from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TrainerBookingBase(BaseModel):
    member_id: int
    trainer_id: int
    booking_datetime: datetime
    status: str = "CONFIRMED"
    training_goal: Optional[str] = None

class TrainerBookingCreate(TrainerBookingBase):
    pass

class TrainerBookingUpdate(BaseModel):
    booking_datetime: Optional[datetime] = None
    status: Optional[str] = None
    training_goal: Optional[str] = None

class TrainerBookingResponse(BaseModel):
    booking_id: int
    member_id: int
    trainer_id: int
    booking_datetime: datetime
    status: str
    training_goal: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
