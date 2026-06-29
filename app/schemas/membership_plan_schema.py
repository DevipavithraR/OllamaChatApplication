from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from decimal import Decimal

class MembershipPlanBase(BaseModel):
    plan_name: str
    duration: str
    price: Decimal
    benefits: Optional[str] = None
    description: Optional[str] = None

class MembershipPlanCreate(MembershipPlanBase):
    pass

class MembershipPlanResponse(MembershipPlanBase):
    plan_id: int
    created_at: datetime

    class Config:
        from_attributes = True
