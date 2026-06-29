from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric, Text
from sqlalchemy.orm import relationship
from app.database import Base

class Booking(Base):
    __tablename__ = "bookings"

    booking_id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.customer_id", ondelete="CASCADE"), nullable=False)
    show_id = Column(Integer, ForeignKey("shows.show_id", ondelete="CASCADE"), nullable=False)
    seat_numbers = Column(Text, nullable=False)
    number_of_tickets = Column(Integer, nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False)
    booking_status = Column(String(50), default="Confirmed", nullable=False)  # Confirmed, Cancelled, Modified
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    customer = relationship("Customer", back_populates="bookings", lazy="joined")
    show = relationship("Show", back_populates="bookings", lazy="joined")
