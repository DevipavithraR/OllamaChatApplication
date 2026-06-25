from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base

class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id", ondelete="CASCADE"), nullable=False)
    reservation_time = Column(DateTime, nullable=False)
    party_size = Column(Integer, nullable=False)
    special_requests = Column(Text, nullable=True)
    status = Column(String(20), default="CONFIRMED", nullable=False)  # e.g., PENDING, CONFIRMED, CANCELLED
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    customer = relationship("Customer", back_populates="reservations")
