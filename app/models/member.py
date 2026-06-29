from sqlalchemy import Column, Integer, String, Date, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Member(Base):
    __tablename__ = "members"

    member_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    phone_number = Column(String(20), nullable=False, unique=True, index=True)
    email = Column(String(100), nullable=True)
    membership_type = Column(String(50), nullable=False, default="Regular")
    registration_date = Column(Date, nullable=False, default=func.current_date())
    created_at = Column(DateTime, nullable=False, default=func.now())

    # Relationships
    issued_books = relationship("IssuedBook", back_populates="member", cascade="all, delete-orphan")
    conversations = relationship("Conversation", back_populates="member")
