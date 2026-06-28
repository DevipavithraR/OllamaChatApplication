from typing import Optional
from sqlalchemy.orm import Session
from app.models.Patient import Patient
from app.repositories.BaseRepository import BaseRepository

class PatientRepository(BaseRepository[Patient]):
    def __init__(self, db: Session):
        super().__init__(Patient, db)

    def get_by_phone_number(self, phone_number: str) -> Optional[Patient]:
        """
        Look up a patient by their phone number.
        """
        return self.db.query(Patient).filter(Patient.phone_number == phone_number).first()
