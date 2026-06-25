from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import settings

# In production, we'd add pool pre-ping and sizing limits to avoid stale connections
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """
    Dependency helper to provide database session lifecycle management.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
