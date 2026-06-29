from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.book import Book
from app.repositories.BookRepository import BookRepository
from app.schemas.book_schema import BookCreate, BookUpdate
from fastapi import HTTPException, status

class BookSearchService:
    def __init__(self, db: Session):
        self.repository = BookRepository(db)

    def create_book(self, book_in: BookCreate) -> Book:
        """
        Create a new book. Raises HTTP 400 if ISBN already exists.
        """
        existing = self.repository.get_by_isbn(book_in.isbn)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Book with ISBN {book_in.isbn} already exists."
            )
        
        book = Book(
            title=book_in.title,
            author=book_in.author,
            category=book_in.category,
            isbn=book_in.isbn,
            publisher=book_in.publisher,
            publication_year=book_in.publication_year,
            available_copies=book_in.available_copies,
            total_copies=book_in.total_copies,
            description=book_in.description
        )
        return self.repository.create(book)

    def get_book_by_id(self, book_id: int) -> Book:
        """
        Retrieve a book by ID. Raises 404 if not found.
        """
        book = self.repository.get(book_id)
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Book with ID {book_id} not found."
            )
        return book

    def get_book_by_title(self, title: str) -> Optional[Book]:
        return self.repository.get_by_title(title)

    def get_book_by_isbn(self, isbn: str) -> Optional[Book]:
        return self.repository.get_by_isbn(isbn)

    def search_books(self, query: str) -> List[Book]:
        return self.repository.search_books(query)

    def get_all_books(self, skip: int = 0, limit: int = 100) -> List[Book]:
        return self.repository.get_all(skip, limit)

    def update_book(self, book_id: int, book_in: BookUpdate) -> Book:
        book = self.get_book_by_id(book_id)
        update_data = book_in.model_dump(exclude_unset=True)
        
        # If isbn is changing, verify uniqueness
        if "isbn" in update_data and update_data["isbn"] != book.isbn:
            existing = self.repository.get_by_isbn(update_data["isbn"])
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Book with ISBN {update_data['isbn']} already exists."
                )

        return self.repository.update(book, update_data)

    def delete_book(self, book_id: int) -> Book:
        self.get_book_by_id(book_id)
        return self.repository.delete(book_id)
