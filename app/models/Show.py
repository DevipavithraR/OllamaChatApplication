from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Show(Base):
    __tablename__ = "shows"

    show_id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey("movies.movie_id", ondelete="CASCADE"), nullable=False)
    theatre_id = Column(Integer, ForeignKey("theatres.theatre_id", ondelete="CASCADE"), nullable=False)
    screen_number = Column(Integer, nullable=False)
    show_datetime = Column(DateTime, nullable=False)
    ticket_price = Column(Numeric(10, 2), nullable=False)
    available_seats = Column(Integer, nullable=False)
    total_seats = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    movie = relationship("Movie", back_populates="shows", lazy="joined")
    theatre = relationship("Theatre", back_populates="shows", lazy="joined")
    bookings = relationship("Booking", back_populates="show", cascade="all, delete-orphan")
