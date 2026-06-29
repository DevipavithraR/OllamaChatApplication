from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class VehicleBase(BaseModel):
    vehicle_number: str = Field(..., min_length=3, max_length=20, examples=["TN69AB1234"])
    vehicle_brand: str = Field(..., min_length=2, max_length=50, examples=["Hyundai"])
    vehicle_model: str = Field(..., min_length=1, max_length=50, examples=["i20"])
    fuel_type: str = Field(..., min_length=2, max_length=20, examples=["Petrol"])
    manufacturing_year: int = Field(..., ge=1900, le=2100, examples=[2023])

class VehicleCreate(VehicleBase):
    customer_id: int

class VehicleUpdate(BaseModel):
    vehicle_number: Optional[str] = Field(None, min_length=3, max_length=20)
    vehicle_brand: Optional[str] = Field(None, min_length=2, max_length=50)
    vehicle_model: Optional[str] = Field(None, min_length=1, max_length=50)
    fuel_type: Optional[str] = Field(None, min_length=2, max_length=20)
    manufacturing_year: Optional[int] = Field(None, ge=1900, le=2100)

class VehicleResponse(VehicleBase):
    vehicle_id: int
    customer_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
