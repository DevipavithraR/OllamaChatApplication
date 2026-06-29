from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.Course import Course
from app.repositories.BaseRepository import BaseRepository

class CourseRepository(BaseRepository[Course]):
    def __init__(self, db: Session):
        super().__init__(Course, db)

    def get_available_courses(self) -> List[Course]:
        """
        Courses that still have seats available.
        """
        return self.db.query(Course).filter(Course.available_seats > 0).all()

    def search_by_name(self, name: str) -> List[Course]:
        return self.db.query(Course).filter(Course.course_name.ilike(f"%{name}%")).all()

    def search_by_eligibility(self, text: str) -> List[Course]:
        return self.db.query(Course).filter(Course.eligibility.ilike(f"%{text}%")).all()

    def get_by_name_exact(self, name: str) -> Optional[Course]:
        return self.db.query(Course).filter(Course.course_name == name).first()
