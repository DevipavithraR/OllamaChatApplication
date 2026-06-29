from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.database import Base

class Member(Base):
    __tablename__ = "members"

    member_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    phone_number = Column(String(20), unique=True, index=True, nullable=False)
    email = Column(String(100), nullable=True)
    gender = Column(String(10), nullable=True)
    age = Column(Integer, nullable=True)
    membership_status = Column(String(20), nullable=False, default="ACTIVE")
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    bookings = relationship("TrainerBooking", back_populates="member", cascade="all, delete-orphan")
    conversations = relationship("Conversation", back_populates="member")
