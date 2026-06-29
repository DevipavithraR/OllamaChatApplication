from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Message(Base):
    __tablename__ = "messages"

    message_id = Column(Integer, primary_key=True, autoincrement=True)
    conversation_id = Column(Integer, ForeignKey("conversations.conversation_id", ondelete="CASCADE"), nullable=False)
    sender = Column(String(20), nullable=False) # 'user' or 'bot'
    message = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())

    # Relationships
    conversation = relationship("Conversation", back_populates="messages")
