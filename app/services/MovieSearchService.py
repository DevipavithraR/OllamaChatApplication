from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.Movie import Movie
from app.models.Theatre import Theatre
from app.models.Show import Show
from app.repositories.MovieRepository import MovieRepository
from app.repositories.TheatreRepository import TheatreRepository
from app.repositories.ShowRepository import ShowRepository
from app.schemas.movie_schema import MovieCreate, MovieUpdate
from app.schemas.theatre_schema import TheatreCreate, TheatreUpdate
from app.schemas.show_schema import ShowCreate, ShowUpdate
from fastapi import HTTPException, status

class MovieSearchService:
    def __init__(self, db: Session):
        self.movie_repo = MovieRepository(db)
        self.theatre_repo = TheatreRepository(db)
        self.show_repo = ShowRepository(db)

    # Movie operations
    def create_movie(self, movie_in: MovieCreate) -> Movie:
        existing = self.movie_repo.get_by_title_exact(movie_in.title)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Movie with title '{movie_in.title}' already exists."
            )
        movie = Movie(**movie_in.model_dump())
        return self.movie_repo.create(movie)

    def get_movie_by_id(self, movie_id: int) -> Movie:
        movie = self.movie_repo.get(movie_id)
        if not movie:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Movie with ID {movie_id} not found."
            )
        return movie

    def get_all_movies(self, skip: int = 0, limit: int = 100) -> List[Movie]:
        return self.movie_repo.get_all(skip, limit)

    def search_movies(self, title: str) -> List[Movie]:
        return self.movie_repo.search_by_title(title)

    def update_movie(self, movie_id: int, movie_in: MovieUpdate) -> Movie:
        movie = self.get_movie_by_id(movie_id)
        update_data = movie_in.model_dump(exclude_unset=True)
        return self.movie_repo.update(movie, update_data)

    def delete_movie(self, movie_id: int) -> Movie:
        movie = self.get_movie_by_id(movie_id)
        return self.movie_repo.delete(movie_id)

    # Theatre operations
    def create_theatre(self, theatre_in: TheatreCreate) -> Theatre:
        existing = self.theatre_repo.get_by_name(theatre_in.theatre_name)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Theatre with name '{theatre_in.theatre_name}' already exists."
            )
        theatre = Theatre(**theatre_in.model_dump())
        return self.theatre_repo.create(theatre)

    def get_theatre_by_id(self, theatre_id: int) -> Theatre:
        theatre = self.theatre_repo.get(theatre_id)
        if not theatre:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Theatre with ID {theatre_id} not found."
            )
        return theatre

    def get_all_theatres(self, skip: int = 0, limit: int = 100) -> List[Theatre]:
        return self.theatre_repo.get_all(skip, limit)

    def update_theatre(self, theatre_id: int, theatre_in: TheatreUpdate) -> Theatre:
        theatre = self.get_theatre_by_id(theatre_id)
        update_data = theatre_in.model_dump(exclude_unset=True)
        return self.theatre_repo.update(theatre, update_data)

    def delete_theatre(self, theatre_id: int) -> Theatre:
        theatre = self.get_theatre_by_id(theatre_id)
        return self.theatre_repo.delete(theatre_id)

    # Show operations
    def create_show(self, show_in: ShowCreate) -> Show:
        # Verify movie and theatre exist
        self.get_movie_by_id(show_in.movie_id)
        self.get_theatre_by_id(show_in.theatre_id)
        show = Show(**show_in.model_dump())
        return self.show_repo.create(show)

    def get_show_by_id(self, show_id: int) -> Show:
        show = self.show_repo.get(show_id)
        if not show:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Show with ID {show_id} not found."
            )
        return show

    def get_all_shows(self, skip: int = 0, limit: int = 100) -> List[Show]:
        return self.show_repo.get_all(skip, limit)

    def get_shows_by_movie(self, movie_id: int) -> List[Show]:
        return self.show_repo.get_shows_by_movie_id(movie_id)

    def get_shows_by_theatre(self, theatre_id: int) -> List[Show]:
        return self.show_repo.get_shows_by_theatre_id(theatre_id)

    def update_show(self, show_id: int, show_in: ShowUpdate) -> Show:
        show = self.get_show_by_id(show_id)
        update_data = show_in.model_dump(exclude_unset=True)
        return self.show_repo.update(show, update_data)

    def delete_show(self, show_id: int) -> Show:
        show = self.get_show_by_id(show_id)
        return self.show_repo.delete(show_id)
