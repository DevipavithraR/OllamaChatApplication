from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.show_schema import ShowCreate, ShowUpdate, ShowResponse
from app.services.MovieSearchService import MovieSearchService

router = APIRouter(prefix="/shows", tags=["Shows"])

@router.post("", response_model=ShowResponse)
def create_show(show: ShowCreate, db: Session = Depends(get_db)):
    service = MovieSearchService(db)
    return service.create_show(show)

@router.get("", response_model=List[ShowResponse])
def get_all_shows(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    service = MovieSearchService(db)
    return service.get_all_shows(skip, limit)

@router.get("/movie/{movie_id}", response_model=List[ShowResponse])
def get_shows_by_movie(movie_id: int, db: Session = Depends(get_db)):
    service = MovieSearchService(db)
    return service.get_shows_by_movie(movie_id)

@router.get("/theatre/{theatre_id}", response_model=List[ShowResponse])
def get_shows_by_theatre(theatre_id: int, db: Session = Depends(get_db)):
    service = MovieSearchService(db)
    return service.get_shows_by_theatre(theatre_id)

@router.get("/{show_id}", response_model=ShowResponse)
def get_show(show_id: int, db: Session = Depends(get_db)):
    service = MovieSearchService(db)
    return service.get_show_by_id(show_id)

@router.put("/{show_id}", response_model=ShowResponse)
def update_show(show_id: int, show: ShowUpdate, db: Session = Depends(get_db)):
    service = MovieSearchService(db)
    return service.update_show(show_id, show)

@router.delete("/{show_id}", response_model=ShowResponse)
def delete_show(show_id: int, db: Session = Depends(get_db)):
    service = MovieSearchService(db)
    return service.delete_show(show_id)
