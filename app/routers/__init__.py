from app.routers.customers import router as customer_router
from app.routers.movies import router as movie_router
from app.routers.theatres import router as theatre_router
from app.routers.shows import router as show_router
from app.routers.bookings import router as booking_router
from app.routers.chatbot import router as chatbot_router

__all__ = [
    "customer_router",
    "movie_router",
    "theatre_router",
    "show_router",
    "booking_router",
    "chatbot_router"
]
