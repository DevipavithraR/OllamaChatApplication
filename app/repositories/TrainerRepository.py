from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.Trainer import Trainer
from app.repositories.BaseRepository import BaseRepository

class TrainerRepository(BaseRepository[Trainer]):
    def __init__(self, db: Session):
        super().__init__(Trainer, db)

    def get_by_name(self, name: str) -> Optional[Trainer]:
        return self.db.query(self.model).filter(self.model.trainer_name == name).first()

    def search_trainers(self, query: str) -> List[Trainer]:
        return self.db.query(self.model).filter(
            self.model.trainer_name.ilike(f"%{query}%") |
            self.model.specialization.ilike(f"%{query}%")
        ).all()
