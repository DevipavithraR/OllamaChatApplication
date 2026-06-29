from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict
from app.schemas.customer_schema import CustomerResponse
from app.schemas.show_schema import ShowResponse

class BookingCreate(BaseModel):
    customer_id: int
    show_id: int
    seat_numbers: List[str]
    number_of_tickets: int
    total_amount: float
    booking_status: Optional[str] = "Confirmed"

class BookingCreateWithCustomer(BaseModel):
    name: str
    phone: str
    email: Optional[str] = None
    show_id: int
    seat_numbers: List[str]
    number_of_tickets: int

class BookingUpdate(BaseModel):
    seat_numbers: Optional[List[str]] = None
    number_of_tickets: Optional[int] = None
    total_amount: Optional[float] = None
    booking_status: Optional[str] = None

class BookingResponse(BaseModel):
    booking_id: int
    customer_id: int
    show_id: int
    seat_numbers: str
    number_of_tickets: int
    total_amount: float
    booking_status: str
    created_at: datetime
    customer: Optional[CustomerResponse] = None
    show: Optional[ShowResponse] = None

    model_config = ConfigDict(from_attributes=True)
