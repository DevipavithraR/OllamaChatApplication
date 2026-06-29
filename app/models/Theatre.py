from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.database import Base

class Theatre(Base):
    __tablename__ = "theatres"

    theatre_id = Column(Integer, primary_key=True, index=True)
    theatre_name = Column(String(100), unique=True, nullable=False)
    location = Column(String(255), nullable=False)
    screens = Column(Integer, default=1, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    shows = relationship("Show", back_populates="theatre", cascade="all, delete-orphan")
