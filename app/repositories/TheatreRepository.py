from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.Theatre import Theatre
from app.repositories.BaseRepository import BaseRepository

class TheatreRepository(BaseRepository[Theatre]):
    def __init__(self, db: Session):
        super().__init__(Theatre, db)

    def get_by_name(self, name: str) -> Optional[Theatre]:
        return self.db.query(Theatre).filter(Theatre.theatre_name.ilike(name)).first()
