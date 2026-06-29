from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Vehicle(Base):
    __tablename__ = "vehicles"

    vehicle_id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.customer_id", ondelete="CASCADE"), nullable=False)
    vehicle_number = Column(String(20), unique=True, index=True, nullable=False)
    vehicle_brand = Column(String(50), nullable=False)
    vehicle_model = Column(String(50), nullable=False)
    fuel_type = Column(String(20), nullable=False)
    manufacturing_year = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    customer = relationship("Customer", back_populates="vehicles")
    bookings = relationship("ServiceBooking", back_populates="vehicle", cascade="all, delete-orphan")
