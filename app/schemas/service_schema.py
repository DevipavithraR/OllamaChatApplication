from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class ServiceCatalogBase(BaseModel):
    service_name: str = Field(..., min_length=2, max_length=100, examples=["General Service"])
    description: Optional[str] = Field(None, examples=["Complete vehicle inspection and service"])
    estimated_duration: str = Field(..., examples=["2 Hours"])
    service_cost: float = Field(..., ge=0, examples=[2500.00])

class ServiceCatalogCreate(ServiceCatalogBase):
    pass

class ServiceCatalogUpdate(BaseModel):
    service_name: Optional[str] = Field(None, min_length=2, max_length=100)
    description: Optional[str] = None
    estimated_duration: Optional[str] = None
    service_cost: Optional[float] = Field(None, ge=0)

class ServiceCatalogResponse(ServiceCatalogBase):
    service_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
