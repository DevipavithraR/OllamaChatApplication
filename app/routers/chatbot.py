from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.chatbot_schema import ChatRequest, ChatResponse, ConversationResponse
from app.services.ChatService import ChatService

router = APIRouter(prefix="/chatbot", tags=["AI Chatbot"])

@router.post("/chat", response_model=ChatResponse, status_code=status.HTTP_200_OK)
def chat_with_assistant(request: ChatRequest, db: Session = Depends(get_db)):
    """
    Interact with the Vehicle Service Center AI Receptionist.
    Maintains a conversation history context of the last 10 messages and uses RAG to fetch service/mechanic details.
    """
    chat_service = ChatService(db)
    result = chat_service.process_message(request.session_id, request.message)
    return ChatResponse(
        session_id=result["session_id"],
        response=result["response"],
        customer_id=result["customer_id"]
    )

@router.get("/history/{session_id}", response_model=ConversationResponse)
def get_session_history(session_id: str, db: Session = Depends(get_db)):
    """
    Retrieve the message history and customer link for a specific session ID.
    """
    chat_service = ChatService(db)
    conversation = chat_service.conversation_repo.get_by_session_id(session_id)
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Conversation history for session '{session_id}' not found."
        )
    return conversation
