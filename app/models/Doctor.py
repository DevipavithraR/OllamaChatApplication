from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Numeric
from sqlalchemy.orm import relationship
from app.database import Base

class Doctor(Base):
    __tablename__ = "doctors"

    doctor_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    department = Column(String(100), nullable=False)
    specialization = Column(String(100), nullable=False, index=True)
    experience = Column(Integer, nullable=False)
    consultation_fee = Column(Numeric(10, 2), nullable=False)
    available_days = Column(String(100), nullable=False)
    available_time = Column(String(100), nullable=False)
    status = Column(String(20), default="ACTIVE", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    appointments = relationship("Appointment", back_populates="doctor", cascade="all, delete-orphan")
