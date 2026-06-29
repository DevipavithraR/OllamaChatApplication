from typing import List
from fastapi import APIRouter, Depends, Query, status, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.mechanic_schema import MechanicCreate, MechanicUpdate, MechanicResponse
from app.repositories.MechanicRepository import MechanicRepository

router = APIRouter(prefix="/mechanics", tags=["Mechanics"])

@router.post("/", response_model=MechanicResponse, status_code=status.HTTP_201_CREATED)
def create_mechanic(mechanic_in: MechanicCreate, db: Session = Depends(get_db)):
    """
    Register a new mechanic.
    """
    repo = MechanicRepository(db)
    from app.models.Mechanic import Mechanic
    mechanic = Mechanic(
        name=mechanic_in.name,
        specialization=mechanic_in.specialization,
        experience=mechanic_in.experience,
        available_status=mechanic_in.available_status
    )
    return repo.create(mechanic)

@router.get("/", response_model=List[MechanicResponse])
def get_mechanics(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Retrieve all mechanics (paginated).
    """
    repo = MechanicRepository(db)
    return repo.get_all(skip, limit)

@router.get("/{mechanic_id}", response_model=MechanicResponse)
def get_mechanic(mechanic_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a mechanic by ID.
    """
    repo = MechanicRepository(db)
    mechanic = repo.get(mechanic_id)
    if not mechanic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Mechanic with ID {mechanic_id} not found."
        )
    return mechanic

@router.put("/{mechanic_id}", response_model=MechanicResponse)
def update_mechanic(mechanic_id: int, mechanic_in: MechanicUpdate, db: Session = Depends(get_db)):
    """
    Update a mechanic's details.
    """
    repo = MechanicRepository(db)
    mechanic = repo.get(mechanic_id)
    if not mechanic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Mechanic with ID {mechanic_id} not found."
        )
    update_data = mechanic_in.model_dump(exclude_unset=True)
    return repo.update(mechanic, update_data)

@router.delete("/{mechanic_id}", response_model=MechanicResponse)
def delete_mechanic(mechanic_id: int, db: Session = Depends(get_db)):
    """
    Remove a mechanic from the system.
    """
    repo = MechanicRepository(db)
    mechanic = repo.get(mechanic_id)
    if not mechanic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Mechanic with ID {mechanic_id} not found."
        )
    return repo.delete(mechanic_id)
