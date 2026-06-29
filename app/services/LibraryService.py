from datetime import date, datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.issued_book import IssuedBook
from app.repositories.IssuedBookRepository import IssuedBookRepository
from app.repositories.BookRepository import BookRepository
from app.repositories.MemberRepository import MemberRepository
from app.schemas.issued_book_schema import IssuedBookCreate, IssuedBookUpdate
from fastapi import HTTPException, status

class LibraryService:
    def __init__(self, db: Session):
        self.repository = IssuedBookRepository(db)
        self.book_repo = BookRepository(db)
        self.member_repo = MemberRepository(db)

    def issue_book(self, dto: IssuedBookCreate) -> IssuedBook:
        """
        Issue a book to a member. Checks availability and decrements available copies.
        """
        member = self.member_repo.get(dto.member_id)
        if not member:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Member with ID {dto.member_id} not found."
            )

        book = self.book_repo.get(dto.book_id)
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Book with ID {dto.book_id} not found."
            )

        if book.available_copies <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Book '{book.title}' has no copies available for issue."
            )

        # Check if already issued and not returned
        already_issued = self.repository.get_active_by_member_and_book(dto.member_id, dto.book_id)
        if already_issued:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Book '{book.title}' is already issued to member {member.name} and not returned yet."
            )

        # Decrement available copies
        book.available_copies -= 1
        self.book_repo.update(book, {"available_copies": book.available_copies})

        # Create issued book record
        issue_date_val = dto.issue_date or date.today()
        issued_book = IssuedBook(
            member_id=dto.member_id,
            book_id=dto.book_id,
            issue_date=issue_date_val,
            due_date=dto.due_date,
            status="Issued"
        )
        return self.repository.create(issued_book)

    def return_book(self, issue_id: int) -> IssuedBook:
        """
        Return a book. Updates status and increments available copies.
        """
        issued_book = self.repository.get(issue_id)
        if not issued_book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Issued book record with ID {issue_id} not found."
            )

        if issued_book.status == "Returned":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Book has already been returned."
            )

        book = self.book_repo.get(issued_book.book_id)
        if book:
            book.available_copies += 1
            self.book_repo.update(book, {"available_copies": book.available_copies})

        # Update return details
        updated = self.repository.update(issued_book, {
            "status": "Returned",
            "return_date": date.today()
        })
        return updated

    def get_due_date_info(self, issue_id: int) -> Optional[IssuedBook]:
        return self.repository.get(issue_id)

    def get_borrowing_history(self, member_id: int) -> List[IssuedBook]:
        return self.repository.get_borrowing_history_by_member(member_id)

    def get_active_issues(self, member_id: int) -> List[IssuedBook]:
        return self.repository.get_active_issues_by_member(member_id)

    def get_all_issues(self, skip: int = 0, limit: int = 100) -> List[IssuedBook]:
        return self.repository.get_all(skip, limit)

    def delete_issue_record(self, issue_id: int) -> IssuedBook:
        issued_book = self.repository.get(issue_id)
        if not issued_book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Issued book record with ID {issue_id} not found."
            )
        # If deleted while still issued, restore the copy
        if issued_book.status == "Issued":
            book = self.book_repo.get(issued_book.book_id)
            if book:
                book.available_copies = min(book.total_copies, book.available_copies + 1)
                self.book_repo.update(book, {"available_copies": book.available_copies})

        return self.repository.delete(issue_id)
