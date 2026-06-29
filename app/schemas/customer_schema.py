from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

class CustomerCreate(BaseModel):
    name: str
    phone_number: str
    email: Optional[str] = None

class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None

class CustomerResponse(BaseModel):
    customer_id: int
    name: str
    phone_number: str
    email: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
