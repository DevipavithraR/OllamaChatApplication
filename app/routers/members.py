from typing import List
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.member_schema import MemberCreate, MemberUpdate, MemberResponse
from app.services.MemberService import MemberService

router = APIRouter(prefix="/members", tags=["Members"])

@router.post("/", response_model=MemberResponse, status_code=status.HTTP_201_CREATED)
def create_member(member_in: MemberCreate, db: Session = Depends(get_db)):
    """
    Register a new library member.
    """
    service = MemberService(db)
    return service.create_member(member_in)

@router.get("/", response_model=List[MemberResponse])
def get_members(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Retrieve all registered members.
    """
    service = MemberService(db)
    return service.get_all_members(skip, limit)

@router.get("/{member_id}", response_model=MemberResponse)
def get_member(member_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a member by ID.
    """
    service = MemberService(db)
    return service.get_member_by_id(member_id)

@router.put("/{member_id}", response_model=MemberResponse)
def update_member(member_id: int, member_in: MemberUpdate, db: Session = Depends(get_db)):
    """
    Update member details.
    """
    service = MemberService(db)
    return service.update_member(member_id, member_in)

@router.delete("/{member_id}", response_model=MemberResponse)
def delete_member(member_id: int, db: Session = Depends(get_db)):
    """
    Delete a member by ID.
    """
    service = MemberService(db)
    return service.delete_member(member_id)
