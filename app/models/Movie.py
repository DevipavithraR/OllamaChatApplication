from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, Date
from sqlalchemy.orm import relationship
from app.database import Base

class Movie(Base):
    __tablename__ = "movies"

    movie_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), unique=True, nullable=False)
    genre = Column(String(100), nullable=False)
    language = Column(String(50), nullable=False)
    duration = Column(String(50), nullable=False)
    rating = Column(String(10), nullable=False)
    description = Column(Text, nullable=True)
    release_date = Column(Date, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    shows = relationship("Show", back_populates="movie", cascade="all, delete-orphan")
