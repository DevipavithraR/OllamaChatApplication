from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class ServiceBookingBase(BaseModel):
    service_date: datetime = Field(..., examples=["2026-07-20 10:00:00"])
    booking_status: str = Field("Scheduled", examples=["Scheduled", "In Progress", "Completed", "Cancelled"])
    customer_notes: Optional[str] = Field(None, examples=["Engine noise during startup"])

class ServiceBookingCreate(ServiceBookingBase):
    customer_id: int
    vehicle_id: int
    mechanic_id: Optional[int] = None
    service_id: int

class ServiceBookingCreateWithCustomer(BaseModel):
    customer_name: str = Field(...)
    customer_phone: str = Field(...)
    customer_email: Optional[str] = None
    vehicle_number: str = Field(...)
    vehicle_brand: Optional[str] = "Unknown"
    vehicle_model: Optional[str] = "Unknown"
    service_name: str = Field(...)
    service_date: datetime = Field(...)
    customer_notes: Optional[str] = None

class ServiceBookingUpdate(BaseModel):
    booking_status: Optional[str] = Field(None)
    mechanic_id: Optional[int] = None
    service_date: Optional[datetime] = None
    estimated_completion: Optional[datetime] = None
    customer_notes: Optional[str] = None

class ServiceBookingResponse(ServiceBookingBase):
    booking_id: int
    customer_id: int
    vehicle_id: int
    mechanic_id: Optional[int]
    service_id: int
    estimated_completion: Optional[datetime]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
