from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.theatre_schema import TheatreCreate, TheatreUpdate, TheatreResponse
from app.services.MovieSearchService import MovieSearchService

router = APIRouter(prefix="/theatres", tags=["Theatres"])

@router.post("", response_model=TheatreResponse)
def create_theatre(theatre: TheatreCreate, db: Session = Depends(get_db)):
    service = MovieSearchService(db)
    return service.create_theatre(theatre)

@router.get("", response_model=List[TheatreResponse])
def get_all_theatres(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    service = MovieSearchService(db)
    return service.get_all_theatres(skip, limit)

@router.get("/{theatre_id}", response_model=TheatreResponse)
def get_theatre(theatre_id: int, db: Session = Depends(get_db)):
    service = MovieSearchService(db)
    return service.get_theatre_by_id(theatre_id)

@router.put("/{theatre_id}", response_model=TheatreResponse)
def update_theatre(theatre_id: int, theatre: TheatreUpdate, db: Session = Depends(get_db)):
    service = MovieSearchService(db)
    return service.update_theatre(theatre_id, theatre)

@router.delete("/{theatre_id}", response_model=TheatreResponse)
def delete_theatre(theatre_id: int, db: Session = Depends(get_db)):
    service = MovieSearchService(db)
    return service.delete_theatre(theatre_id)
