import logging
from typing import List
from sqlalchemy.orm import Session
from app.models.Course import Course
from app.models.Department import Department
from app.repositories.CourseRepository import CourseRepository
from app.repositories.DepartmentRepository import DepartmentRepository

logger = logging.getLogger("app.services.CourseSearchService")

class CourseSearchService:
    def __init__(self, db: Session):
        self.db = db
        self.course_repo = CourseRepository(db)
        self.department_repo = DepartmentRepository(db)

    def search_courses(self, user_query: str) -> List[Course]:
        """
        Retrieves courses matching user search keywords (e.g. course name, department name, eligibility keyword).
        """
        if not user_query:
            return []

        query_lower = user_query.lower()
        
        # Pull all courses and filter locally to enable flexible semantic/substring matching
        all_courses = self.course_repo.get_all(limit=100)
        matched = []

        for course in all_courses:
            # Check course name
            if course.course_name.lower() in query_lower or query_lower in course.course_name.lower():
                matched.append(course)
                continue
            
            # Check department name
            if course.department and (course.department.department_name.lower() in query_lower or query_lower in course.department.department_name.lower()):
                matched.append(course)
                continue

            # Check eligibility text
            if course.eligibility.lower() in query_lower or query_lower in course.eligibility.lower():
                matched.append(course)
                continue

            # Check description keywords
            if course.description and any(word in course.description.lower() for word in query_lower.split() if len(word) > 3):
                matched.append(course)
                continue

        # If still empty, do standard database substring queries
        if not matched:
            # Simple fallback search by parts of name
            for word in query_lower.split():
                if len(word) > 3:
                    sub_match = self.course_repo.search_by_name(word)
                    if sub_match:
                        matched.extend(sub_match)
            # Remove duplicates preserving order
            seen = set()
            matched = [x for x in matched if not (x.course_id in seen or seen.add(x.course_id))]

        return matched

    def get_available_courses(self) -> List[Course]:
        return self.course_repo.get_available_courses()

    def get_all_courses(self) -> List[Course]:
        return self.course_repo.get_all(limit=100)

    def get_all_departments(self) -> List[Department]:
        return self.department_repo.get_all(limit=100)

    def get_department_by_name(self, name: str) -> Department:
        from fastapi import HTTPException, status
        dept = self.department_repo.get_by_name(name)
        if not dept:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Department with name '{name}' not found."
            )
        return dept
