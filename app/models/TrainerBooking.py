from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class TrainerBooking(Base):
    __tablename__ = "trainer_bookings"

    booking_id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("members.member_id", ondelete="CASCADE"), nullable=False)
    trainer_id = Column(Integer, ForeignKey("trainers.trainer_id", ondelete="CASCADE"), nullable=False)
    booking_datetime = Column(DateTime, nullable=False)
    status = Column(String(20), nullable=False, default="CONFIRMED")
    training_goal = Column(String(200), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    member = relationship("Member", back_populates="bookings")
    trainer = relationship("Trainer", back_populates="bookings")
