from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class CustomerBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, examples=["Rahul Kumar"])
    phone_number: str = Field(..., min_length=7, max_length=20, examples=["+919876543210"])
    email: Optional[str] = Field(None, examples=["rahul.kumar@example.com"])
    address: Optional[str] = Field(None, examples=["123 Main St, Chennai"])

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    phone_number: Optional[str] = Field(None, min_length=7, max_length=20)
    email: Optional[str] = None
    address: Optional[str] = None

class CustomerResponse(CustomerBase):
    customer_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
