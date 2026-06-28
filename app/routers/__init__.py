from app.routers.patients import router as patient_router
from app.routers.doctors import router as doctor_router
from app.routers.departments import router as department_router
from app.routers.appointments import router as appointment_router
from app.routers.chatbot import router as chatbot_router

__all__ = [
    "patient_router",
    "doctor_router",
    "department_router",
    "appointment_router",
    "chatbot_router"
]
