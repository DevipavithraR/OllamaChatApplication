from typing import List
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.issued_book_schema import IssuedBookCreate, IssuedBookUpdate, IssuedBookResponse
from app.services.LibraryService import LibraryService

router = APIRouter(prefix="/issued_books", tags=["Issued Books"])

def format_issue(issue) -> IssuedBookResponse:
    return IssuedBookResponse(
        issue_id=issue.issue_id,
        member_id=issue.member_id,
        book_id=issue.book_id,
        issue_date=issue.issue_date,
        due_date=issue.due_date,
        return_date=issue.return_date,
        status=issue.status,
        created_at=issue.created_at,
        member_name=issue.member.name if issue.member else f"Member #{issue.member_id}",
        book_title=issue.book.title if issue.book else f"Book #{issue.book_id}"
    )

@router.post("/", response_model=IssuedBookResponse, status_code=status.HTTP_201_CREATED)
def issue_book(dto: IssuedBookCreate, db: Session = Depends(get_db)):
    """
    Issue a book.
    """
    service = LibraryService(db)
    issue = service.issue_book(dto)
    return format_issue(issue)

@router.get("/", response_model=List[IssuedBookResponse])
def get_all_issues(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Retrieve all issued book records.
    """
    service = LibraryService(db)
    issues = service.get_all_issues(skip, limit)
    return [format_issue(i) for i in issues]

@router.get("/{issue_id}", response_model=IssuedBookResponse)
def get_issue(issue_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific issue record by ID.
    """
    service = LibraryService(db)
    issue = service.get_due_date_info(issue_id)
    return format_issue(issue)

@router.put("/{issue_id}", response_model=IssuedBookResponse)
def return_book(issue_id: int, db: Session = Depends(get_db)):
    """
    Return an issued book.
    """
    service = LibraryService(db)
    issue = service.return_book(issue_id)
    return format_issue(issue)

@router.delete("/{issue_id}", response_model=IssuedBookResponse)
def delete_issue_record(issue_id: int, db: Session = Depends(get_db)):
    """
    Delete an issue record by ID.
    """
    service = LibraryService(db)
    issue = service.delete_issue_record(issue_id)
    return format_issue(issue)
