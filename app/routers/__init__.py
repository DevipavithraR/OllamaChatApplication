from app.routers.customer import router as customer_router
from app.routers.reservation import router as reservation_router
from app.routers.menu import router as menu_router
from app.routers.chatbot import router as chatbot_router

__all__ = [
    "customer_router",
    "reservation_router",
    "menu_router",
    "chatbot_router"
]
