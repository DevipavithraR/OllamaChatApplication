from typing import List
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.book_schema import BookCreate, BookUpdate, BookResponse
from app.services.BookSearchService import BookSearchService

router = APIRouter(prefix="/books", tags=["Books"])

@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(book_in: BookCreate, db: Session = Depends(get_db)):
    """
    Add a new book to the library database.
    """
    service = BookSearchService(db)
    return service.create_book(book_in)

@router.get("/", response_model=List[BookResponse])
def get_books(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Retrieve all books.
    """
    service = BookSearchService(db)
    return service.get_all_books(skip, limit)

@router.get("/search", response_model=List[BookResponse])
def search_books(q: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    """
    Search books dynamically.
    """
    service = BookSearchService(db)
    return service.search_books(q)

@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a book by ID.
    """
    service = BookSearchService(db)
    return service.get_book_by_id(book_id)

@router.put("/{book_id}", response_model=BookResponse)
def update_book(book_id: int, book_in: BookUpdate, db: Session = Depends(get_db)):
    """
    Update an existing book record.
    """
    service = BookSearchService(db)
    return service.update_book(book_id, book_in)

@router.delete("/{book_id}", response_model=BookResponse)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """
    Delete a book by ID.
    """
    service = BookSearchService(db)
    return service.delete_book(book_id)
