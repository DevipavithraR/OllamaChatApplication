from app.routers.students import router as student_router
from app.routers.courses import router as course_router
from app.routers.departments import router as department_router
from app.routers.admissions import router as admission_router
from app.routers.chatbot import router as chatbot_router

__all__ = [
    "student_router",
    "course_router",
    "department_router",
    "admission_router",
    "chatbot_router"
]
