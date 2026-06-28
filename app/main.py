import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine, Base
from app.routers import patient_router, doctor_router, department_router, appointment_router, chatbot_router
from app.exceptions.handlers import setup_exception_handlers

# Configure logging format and level
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("app.main")

# Auto-create tables on startup if they don't exist
# In professional environments, migrations (e.g. Alembic) are used,
# but auto-creation provides immediate setup utility.
try:
    logger.info("Initializing database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables initialized successfully.")
except Exception as e:
    logger.error(f"Error initializing database tables: {str(e)}")

app = FastAPI(
    title="Hospital AI Appointment Receptionist API",
    description="FastAPI service for hospital operations and an interactive RAG receptionist chatbot.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware for frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup global exception mapping handlers
setup_exception_handlers(app)

# Include API Routers
app.include_router(patient_router)
app.include_router(doctor_router)
app.include_router(department_router)
app.include_router(appointment_router)
app.include_router(chatbot_router)

@app.get("/")
def read_root():
    return {
        "app": "Hope Hospital AI Appointment Receptionist API",
        "version": "1.0.0",
        "status": "healthy",
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting server on {settings.HOST}:{settings.PORT}...")
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=True)
