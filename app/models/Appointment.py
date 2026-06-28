from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base

class Appointment(Base):
    __tablename__ = "appointments"

    appointment_id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.patient_id", ondelete="CASCADE"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctors.doctor_id", ondelete="CASCADE"), nullable=False)
    appointment_datetime = Column(DateTime, nullable=False)
    status = Column(String(20), default="CONFIRMED", nullable=False)  # CONFIRMED, CANCELLED, RESCHEDULED
    special_notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    patient = relationship("Patient", back_populates="appointments", lazy="joined")
    doctor = relationship("Doctor", back_populates="appointments", lazy="joined")
