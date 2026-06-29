from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.Movie import Movie
from app.repositories.BaseRepository import BaseRepository

class MovieRepository(BaseRepository[Movie]):
    def __init__(self, db: Session):
        super().__init__(Movie, db)

    def search_by_title(self, title: str) -> List[Movie]:
        return self.db.query(Movie).filter(Movie.title.ilike(f"%{title}%")).all()

    def get_by_title_exact(self, title: str) -> Optional[Movie]:
        return self.db.query(Movie).filter(Movie.title == title).first()
