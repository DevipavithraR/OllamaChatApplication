from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.Show import Show
from app.repositories.BaseRepository import BaseRepository

class ShowRepository(BaseRepository[Show]):
    def __init__(self, db: Session):
        super().__init__(Show, db)

    def get_shows_by_movie_id(self, movie_id: int) -> List[Show]:
        return self.db.query(Show).filter(Show.movie_id == movie_id).all()

    def get_shows_by_theatre_id(self, theatre_id: int) -> List[Show]:
        return self.db.query(Show).filter(Show.theatre_id == theatre_id).all()
