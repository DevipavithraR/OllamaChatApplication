from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.book import Book
from app.repositories.BaseRepository import BaseRepository

class BookRepository(BaseRepository[Book]):
    def __init__(self, db: Session):
        super().__init__(Book, db)

    def get_by_isbn(self, isbn: str) -> Optional[Book]:
        return self.db.query(Book).filter(Book.isbn == isbn).first()

    def get_by_title(self, title: str) -> Optional[Book]:
        return self.db.query(Book).filter(Book.title.ilike(title)).first()

    def search_books(self, query: str) -> List[Book]:
        if not query:
            return []
        q = f"%{query}%"
        return self.db.query(Book).filter(
            Book.title.ilike(q) |
            Book.author.ilike(q) |
            Book.category.ilike(q) |
            Book.publisher.ilike(q) |
            Book.description.ilike(q)
        ).all()
