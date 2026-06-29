import pytest
from unittest.mock import MagicMock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.database import Base, get_db
from app.main import app
from app.services.OllamaService import OllamaService

# Use an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """
    Creates an isolated database session for a single test.
    """
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    """
    Returns a FastAPI TestClient configured to use the mock database session.
    """
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
def mock_ollama(monkeypatch):
    """
    Mocks the OllamaService class to return pre-defined responses.
    """
    mock_chat = MagicMock(return_value="Hello! I am the gym receptionist chatbot. How can I assist you?")
    mock_emb = MagicMock(return_value=[0.1, 0.2, 0.3])
    
    monkeypatch.setattr(OllamaService, "chat", mock_chat)
    monkeypatch.setattr(OllamaService, "get_embedding", mock_emb)
    
    return {
        "chat": mock_chat,
        "get_embedding": mock_emb
    }
