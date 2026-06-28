from typing import Optional
from sqlalchemy.orm import Session
from app.models.Department import Department
from app.repositories.BaseRepository import BaseRepository

class DepartmentRepository(BaseRepository[Department]):
    def __init__(self, db: Session):
        super().__init__(Department, db)

    def get_by_name(self, name: str) -> Optional[Department]:
        """
        Get department by name.
        """
        return self.db.query(Department).filter(Department.department_name.ilike(name)).first()
