from typing import List
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.membership_plan_schema import MembershipPlanCreate, MembershipPlanResponse
from app.services.MembershipService import MembershipService

router = APIRouter(prefix="/plans", tags=["Membership Plans"])

@router.post("/", response_model=MembershipPlanResponse, status_code=status.HTTP_201_CREATED)
def create_plan(plan_in: MembershipPlanCreate, db: Session = Depends(get_db)):
    """
    Create a new membership plan.
    """
    service = MembershipService(db)
    return service.create_plan(plan_in)

@router.get("/", response_model=List[MembershipPlanResponse])
def get_plans(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Retrieve all membership plans.
    """
    service = MembershipService(db)
    return service.get_all_plans(skip, limit)

@router.get("/search", response_model=List[MembershipPlanResponse])
def search_plans(q: str = Query(...), db: Session = Depends(get_db)):
    """
    Search membership plans by keyword.
    """
    service = MembershipService(db)
    return service.search_plans(q)

@router.get("/{plan_id}", response_model=MembershipPlanResponse)
def get_plan(plan_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a plan by ID.
    """
    service = MembershipService(db)
    return service.get_plan_by_id(plan_id)
