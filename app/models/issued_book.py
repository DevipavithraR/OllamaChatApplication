from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class IssuedBook(Base):
    __tablename__ = "issued_books"

    issue_id = Column(Integer, primary_key=True, autoincrement=True)
    member_id = Column(Integer, ForeignKey("members.member_id", ondelete="CASCADE"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.book_id", ondelete="CASCADE"), nullable=False)
    issue_date = Column(Date, nullable=False, default=func.current_date())
    due_date = Column(Date, nullable=False)
    return_date = Column(Date, nullable=True)
    status = Column(String(20), nullable=False, default="Issued")
    created_at = Column(DateTime, nullable=False, default=func.now())

    # Relationships
    member = relationship("Member", back_populates="issued_books")
    book = relationship("Book", back_populates="issued_records")
