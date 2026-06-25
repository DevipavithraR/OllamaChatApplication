from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class CustomerBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, examples=["John Doe"])
    phone: str = Field(..., min_length=7, max_length=20, examples=["+1234567890"])
    email: Optional[str] = Field(None, examples=["john.doe@example.com"])

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    phone: Optional[str] = Field(None, min_length=7, max_length=20)
    email: Optional[str] = None

class CustomerResponse(CustomerBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
