from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from app.schemas.customer import CustomerResponse

class ReservationBase(BaseModel):
    reservation_time: datetime = Field(..., examples=["2026-07-01T19:00:00"])
    party_size: int = Field(..., ge=1, le=20, examples=[4])
    special_requests: Optional[str] = Field(None, max_length=500, examples=["Window seat, high chair for toddler"])
    status: str = Field("CONFIRMED", max_length=20, examples=["CONFIRMED"])

class ReservationCreate(ReservationBase):
    customer_id: int

class ReservationCreateWithCustomer(ReservationBase):
    customer_name: str = Field(..., min_length=2, max_length=100, examples=["John Doe"])
    customer_phone: str = Field(..., min_length=7, max_length=20, examples=["+1234567890"])
    customer_email: Optional[str] = Field(None, examples=["john.doe@example.com"])

class ReservationUpdate(BaseModel):
    reservation_time: Optional[datetime] = None
    party_size: Optional[int] = Field(None, ge=1, le=20)
    special_requests: Optional[str] = None
    status: Optional[str] = None

class ReservationResponse(ReservationBase):
    id: int
    customer_id: int
    created_at: datetime
    customer: Optional[CustomerResponse] = None

    model_config = ConfigDict(from_attributes=True)
