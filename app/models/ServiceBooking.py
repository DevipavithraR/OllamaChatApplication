from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class ServiceBooking(Base):
    __tablename__ = "service_bookings"

    booking_id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.customer_id", ondelete="CASCADE"), nullable=False)
    vehicle_id = Column(Integer, ForeignKey("vehicles.vehicle_id", ondelete="CASCADE"), nullable=False)
    mechanic_id = Column(Integer, ForeignKey("mechanics.mechanic_id", ondelete="SET NULL"), nullable=True)
    service_id = Column(Integer, ForeignKey("service_catalog.service_id", ondelete="CASCADE"), nullable=False)
    service_date = Column(DateTime, nullable=False)
    booking_status = Column(String(20), default="Scheduled", nullable=False)
    estimated_completion = Column(DateTime, nullable=True)
    customer_notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    customer = relationship("Customer", back_populates="bookings")
    vehicle = relationship("Vehicle", back_populates="bookings")
    mechanic = relationship("Mechanic", back_populates="bookings")
    service = relationship("ServiceCatalog", back_populates="bookings")
