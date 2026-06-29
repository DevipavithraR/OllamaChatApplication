from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Date
from sqlalchemy.orm import relationship
from app.database import Base

class Admission(Base):
    __tablename__ = "admissions"

    admission_id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.student_id", ondelete="CASCADE"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.course_id", ondelete="CASCADE"), nullable=False)
    application_date = Column(Date, nullable=False)
    status = Column(String(50), default="Pending Verification", nullable=False)  # Pending Verification, Verified, Cancelled
    remarks = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    student = relationship("Student", back_populates="admissions", lazy="joined")
    course = relationship("Course", back_populates="admissions", lazy="joined")
