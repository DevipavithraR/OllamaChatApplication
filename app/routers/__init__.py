from app.routers.members import router as member_router
from app.routers.plans import router as plan_router
from app.routers.trainers import router as trainer_router
from app.routers.trainer_bookings import router as booking_router
from app.routers.chatbot import router as chatbot_router

__all__ = [
    "member_router",
    "plan_router",
    "trainer_router",
    "booking_router",
    "chatbot_router"
]
