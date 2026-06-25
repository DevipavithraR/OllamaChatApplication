from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class MenuItemBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, examples=["Margherita Pizza"])
    description: Optional[str] = Field(None, max_length=1000, examples=["Fresh mozzarella, basil, and tomato sauce."])
    price: Decimal = Field(..., ge=0.0, decimal_places=2, examples=[14.99])
    category: str = Field(..., min_length=2, max_length=50, examples=["entrees"])
    is_available: bool = Field(True, examples=[True])

class MenuItemCreate(MenuItemBase):
    pass

class MenuItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Decimal] = None
    category: Optional[str] = None
    is_available: Optional[bool] = None

class MenuItemResponse(MenuItemBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
