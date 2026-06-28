from typing import List, Optional
from sqlalchemy import or_
from sqlalchemy.orm import Session
from app.models.Doctor import Doctor
from app.repositories.BaseRepository import BaseRepository

class DoctorRepository(BaseRepository[Doctor]):
    def __init__(self, db: Session):
        super().__init__(Doctor, db)

    def get_by_name(self, name: str) -> Optional[Doctor]:
        """
        Look up a doctor by name (case-insensitive, exact or partial match).
        """
        # Exact match
        res = self.db.query(Doctor).filter(Doctor.name.ilike(name)).first()
        if res:
            return res
        # If no exact match, try stripping prefix like 'Dr.' or 'Dr. '
        clean_name = name.lower().replace("dr.", "").strip()
        return self.db.query(Doctor).filter(Doctor.name.ilike(f"%{clean_name}%")).first()

    def get_active_doctors(self) -> List[Doctor]:
        """
        Get all doctors currently marked as ACTIVE.
        """
        return self.db.query(Doctor).filter(Doctor.status == "ACTIVE").all()

    def search_by_keywords(self, keywords: List[str]) -> List[Doctor]:
        """
        Search for active doctors matching keywords in name, specialization, or department.
        """
        if not keywords:
            return []

        filters = []
        for kw in keywords:
            if kw.strip():
                pattern = f"%{kw.strip()}%"
                filters.append(Doctor.name.ilike(pattern))
                filters.append(Doctor.specialization.ilike(pattern))
                filters.append(Doctor.department.ilike(pattern))

        if not filters:
            return []

        return (
            self.db.query(Doctor)
            .filter(Doctor.status == "ACTIVE")
            .filter(or_(*filters))
            .limit(10)
            .all()
        )
