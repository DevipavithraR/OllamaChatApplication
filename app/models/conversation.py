from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Conversation(Base):
    __tablename__ = "conversations"

    conversation_id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(100), nullable=False, unique=True, index=True)
    member_id = Column(Integer, ForeignKey("members.member_id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime, nullable=False, default=func.now())

    # Relationships
    member = relationship("Member", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")
