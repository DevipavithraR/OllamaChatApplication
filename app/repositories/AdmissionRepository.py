from typing import List
from sqlalchemy import and_
from sqlalchemy.orm import Session
from app.models.Admission import Admission
from app.repositories.BaseRepository import BaseRepository

class AdmissionRepository(BaseRepository[Admission]):
    def __init__(self, db: Session):
        super().__init__(Admission, db)

    def get_by_student_id(self, student_id: int) -> List[Admission]:
        return self.db.query(Admission).filter(Admission.student_id == student_id).all()

    def get_active_by_student_id(self, student_id: int) -> List[Admission]:
        """
        Admissions that are not cancelled.
        """
        return self.db.query(Admission).filter(
            and_(
                Admission.student_id == student_id,
                Admission.status != "Cancelled"
            )
        ).all()
