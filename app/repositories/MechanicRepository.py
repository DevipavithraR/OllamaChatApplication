from typing import List, Optional
from sqlalchemy import or_
from sqlalchemy.orm import Session
from app.models.Mechanic import Mechanic
from app.repositories.BaseRepository import BaseRepository

class MechanicRepository(BaseRepository[Mechanic]):
    def __init__(self, db: Session):
        super().__init__(Mechanic, db)

    def get_available_mechanics(self) -> List[Mechanic]:
        """
        Get all mechanics who are currently marked as available.
        """
        return self.db.query(Mechanic).filter(Mechanic.available_status == "Available").all()

    def search_mechanics(self, keywords: List[str]) -> List[Mechanic]:
        """
        Search mechanics by specialization or name matching any keywords.
        """
        if not keywords:
            return []
        
        filters = []
        for kw in keywords:
            if kw.strip():
                pattern = f"%{kw.strip()}%"
                filters.append(Mechanic.name.ilike(pattern))
                filters.append(Mechanic.specialization.ilike(pattern))

        if not filters:
            return []

        return (
            self.db.query(Mechanic)
            .filter(or_(*filters))
            .limit(10)
            .all()
        )
