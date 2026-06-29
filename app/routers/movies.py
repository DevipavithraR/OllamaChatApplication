from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.movie_schema import MovieCreate, MovieUpdate, MovieResponse
from app.services.MovieSearchService import MovieSearchService

router = APIRouter(prefix="/movies", tags=["Movies"])

@router.post("", response_model=MovieResponse)
def create_movie(movie: MovieCreate, db: Session = Depends(get_db)):
    service = MovieSearchService(db)
    return service.create_movie(movie)

@router.get("", response_model=List[MovieResponse])
def get_all_movies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    service = MovieSearchService(db)
    return service.get_all_movies(skip, limit)

@router.get("/search", response_model=List[MovieResponse])
def search_movies(title: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    service = MovieSearchService(db)
    return service.search_movies(title)

@router.get("/{movie_id}", response_model=MovieResponse)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    service = MovieSearchService(db)
    return service.get_movie_by_id(movie_id)

@router.put("/{movie_id}", response_model=MovieResponse)
def update_movie(movie_id: int, movie: MovieUpdate, db: Session = Depends(get_db)):
    service = MovieSearchService(db)
    return service.update_movie(movie_id, movie)

@router.delete("/{movie_id}", response_model=MovieResponse)
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    service = MovieSearchService(db)
    return service.delete_movie(movie_id)
