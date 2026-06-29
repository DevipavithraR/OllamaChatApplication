from app.routers.customers import router as customer_router
from app.routers.vehicles import router as vehicle_router
from app.routers.mechanics import router as mechanic_router
from app.routers.services import router as service_router
from app.routers.service_bookings import router as service_booking_router
from app.routers.chatbot import router as chatbot_router

__all__ = [
    "customer_router",
    "vehicle_router",
    "mechanic_router",
    "service_router",
    "service_booking_router",
    "chatbot_router"
]
