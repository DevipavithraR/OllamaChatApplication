from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Numeric
from sqlalchemy.orm import relationship
from app.database import Base

class Trainer(Base):
    __tablename__ = "trainers"

    trainer_id = Column(Integer, primary_key=True, index=True)
    trainer_name = Column(String(100), unique=True, index=True, nullable=False)
    specialization = Column(String(200), nullable=False)
    experience = Column(String(50), nullable=False)
    available_days = Column(String(100), nullable=False)
    available_time = Column(String(100), nullable=False)
    session_fee = Column(Numeric(10, 2), nullable=False)
    status = Column(String(20), nullable=False, default="ACTIVE")
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    bookings = relationship("TrainerBooking", back_populates="trainer", cascade="all, delete-orphan")
