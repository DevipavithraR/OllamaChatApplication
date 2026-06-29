from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Numeric, Text
from app.database import Base

class MembershipPlan(Base):
    __tablename__ = "membership_plans"

    plan_id = Column(Integer, primary_key=True, index=True)
    plan_name = Column(String(100), unique=True, index=True, nullable=False)
    duration = Column(String(50), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    benefits = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
