from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.issued_book import IssuedBook
from app.repositories.BaseRepository import BaseRepository

class IssuedBookRepository(BaseRepository[IssuedBook]):
    def __init__(self, db: Session):
        super().__init__(IssuedBook, db)

    def get_active_issues_by_member(self, member_id: int) -> List[IssuedBook]:
        return (
            self.db.query(IssuedBook)
            .filter(IssuedBook.member_id == member_id, IssuedBook.status == "Issued")
            .order_by(IssuedBook.issue_date.desc())
            .all()
        )

    def get_borrowing_history_by_member(self, member_id: int) -> List[IssuedBook]:
        return (
            self.db.query(IssuedBook)
            .filter(IssuedBook.member_id == member_id)
            .order_by(IssuedBook.issue_date.desc())
            .all()
        )

    def get_active_by_member_and_book(self, member_id: int, book_id: int) -> Optional[IssuedBook]:
        return (
            self.db.query(IssuedBook)
            .filter(
                IssuedBook.member_id == member_id,
                IssuedBook.book_id == book_id,
                IssuedBook.status == "Issued"
            )
            .first()
        )
