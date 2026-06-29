from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.chatbot import ChatRequest, ChatResponse
from app.schemas.conversation_schema import ConversationResponse
from app.services.ChatService import ChatService

router = APIRouter(prefix="/chatbot", tags=["Chatbot"])

@router.post("/chat", response_model=ChatResponse)
def chat_with_bot(payload: ChatRequest, db: Session = Depends(get_db)):
    """
    Send a message to the Digital Library Assistant and receive a processed response.
    """
    service = ChatService(db)
    result = service.process_message(payload.session_id, payload.message)
    return ChatResponse(
        session_id=result["session_id"],
        response=result["response"],
        member_id=result["member_id"],
        customer_id=result["customer_id"]
    )

@router.get("/history/{session_id}", response_model=ConversationResponse)
def get_chat_history(session_id: str, db: Session = Depends(get_db)):
    """
    Retrieve conversational message logs for a given session.
    """
    service = ChatService(db)
    conversation = service.get_conversation_history(session_id)
    return conversation
