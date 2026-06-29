from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Numeric, DateTime
from sqlalchemy.orm import relationship
from app.database import Base

class ServiceCatalog(Base):
    __tablename__ = "service_catalog"

    service_id = Column(Integer, primary_key=True, index=True)
    service_name = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    estimated_duration = Column(String(50), nullable=False)
    service_cost = Column(Numeric(10, 2), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    bookings = relationship("ServiceBooking", back_populates="service", cascade="all, delete-orphan")
