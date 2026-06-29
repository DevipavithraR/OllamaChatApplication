from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Book(Base):
    __tablename__ = "books"

    book_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    author = Column(String(100), nullable=False)
    category = Column(String(100), nullable=False)
    isbn = Column(String(20), nullable=False, unique=True, index=True)
    publisher = Column(String(100), nullable=False)
    publication_year = Column(Integer, nullable=False)
    available_copies = Column(Integer, nullable=False)
    total_copies = Column(Integer, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, default=func.now())

    # Relationships
    issued_records = relationship("IssuedBook", back_populates="book", cascade="all, delete-orphan")
