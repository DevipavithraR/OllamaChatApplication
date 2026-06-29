from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.database import Base

class Mechanic(Base):
    __tablename__ = "mechanics"

    mechanic_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    specialization = Column(String(100), nullable=False)
    experience = Column(Integer, nullable=False)
    available_status = Column(String(20), default="Available", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    bookings = relationship("ServiceBooking", back_populates="mechanic")
