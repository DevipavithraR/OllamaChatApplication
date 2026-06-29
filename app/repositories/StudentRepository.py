from typing import Optional
from sqlalchemy.orm import Session
from app.models.Student import Student
from app.repositories.BaseRepository import BaseRepository

class StudentRepository(BaseRepository[Student]):
    def __init__(self, db: Session):
        super().__init__(Student, db)

    def get_by_phone_number(self, phone_number: str) -> Optional[Student]:
        """
        Look up a student by their phone number.
        """
        return self.db.query(Student).filter(Student.phone_number == phone_number).first()
