from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.conversation_schema import ChatRequest, ChatResponse, ConversationHistoryResponse
from app.services.ChatService import ChatService
from app.repositories.ConversationRepository import ConversationRepository

router = APIRouter(prefix="/chatbot", tags=["Chatbot Receptionist"])

@router.post("/chat", response_model=ChatResponse)
def chat_with_bot(payload: ChatRequest, db: Session = Depends(get_db)):
    """
    Send a message to the AI Gym Receptionist.
    """
    service = ChatService(db)
    result = service.process_message(payload.session_id, payload.message)
    return ChatResponse(
        session_id=result["session_id"],
        response=result["response"],
        member_id=result["member_id"]
    )

@router.get("/history/{session_id}", response_model=ConversationHistoryResponse)
def get_chat_history(session_id: str, db: Session = Depends(get_db)):
    """
    Retrieve conversational message history for a session ID.
    """
    repo = ConversationRepository(db)
    conversation = repo.get_by_session_id(session_id)
    if not conversation:
        # Create empty conversation
        from app.models.Conversation import Conversation as ConversationModel
        conversation = ConversationModel(session_id=session_id)
        conversation = repo.create(conversation)
    
    # Refresh to load messages
    db.refresh(conversation)
    
    # Retrieve messages
    messages = repo.get_last_n_messages(conversation.conversation_id, limit=20)
    
    return ConversationHistoryResponse(
        conversation_id=conversation.conversation_id,
        session_id=conversation.session_id,
        member_id=conversation.member_id,
        created_at=conversation.created_at,
        messages=messages
    )
