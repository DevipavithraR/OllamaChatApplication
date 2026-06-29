from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Date, Numeric, Text
from sqlalchemy.orm import relationship
from app.database import Base

class Student(Base):
    __tablename__ = "students"

    student_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    phone_number = Column(String(20), unique=True, index=True, nullable=False)
    email = Column(String(100), nullable=True)
    date_of_birth = Column(Date, nullable=True)
    gender = Column(String(10), nullable=True)
    address = Column(Text, nullable=True)
    marks_percentage = Column(Numeric(5, 2), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    admissions = relationship("Admission", back_populates="student", cascade="all, delete-orphan")
    conversations = relationship("Conversation", back_populates="student")
