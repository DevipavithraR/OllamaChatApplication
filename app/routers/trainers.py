from typing import List
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.trainer_schema import TrainerCreate, TrainerUpdate, TrainerResponse
from app.services.TrainerSearchService import TrainerSearchService

router = APIRouter(prefix="/trainers", tags=["Trainers"])

@router.post("/", response_model=TrainerResponse, status_code=status.HTTP_201_CREATED)
def create_trainer(trainer_in: TrainerCreate, db: Session = Depends(get_db)):
    """
    Create a new personal trainer.
    """
    service = TrainerSearchService(db)
    return service.create_trainer(trainer_in)

@router.get("/", response_model=List[TrainerResponse])
def get_trainers(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Retrieve all trainers.
    """
    service = TrainerSearchService(db)
    return service.get_all_trainers(skip, limit)

@router.get("/search", response_model=List[TrainerResponse])
def search_trainers(q: str = Query(...), db: Session = Depends(get_db)):
    """
    Search trainers by specialization or name.
    """
    service = TrainerSearchService(db)
    return service.search_trainers(q)

@router.get("/{trainer_id}", response_model=TrainerResponse)
def get_trainer(trainer_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a trainer by ID.
    """
    service = TrainerSearchService(db)
    return service.get_trainer_by_id(trainer_id)

@router.put("/{trainer_id}", response_model=TrainerResponse)
def update_trainer(trainer_id: int, trainer_in: TrainerUpdate, db: Session = Depends(get_db)):
    """
    Update trainer details (e.g. status, session fee, available days).
    """
    service = TrainerSearchService(db)
    return service.update_trainer(trainer_id, trainer_in)
