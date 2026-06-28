from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.conversation_schema import ChatRequest, ChatResponse, ConversationResponse
from app.services.ChatService import ChatService
from app.repositories.ConversationRepository import ConversationRepository
from app.repositories.MessageRepository import MessageRepository

router = APIRouter(prefix="/chatbot", tags=["Chatbot"])

@router.post("/chat", response_model=ChatResponse)
def chat(chat_req: ChatRequest, db: Session = Depends(get_db)):
    service = ChatService(db)
    result = service.process_message(chat_req.session_id, chat_req.message)
    return ChatResponse(
        session_id=result["session_id"],
        response=result["response"],
        patient_id=result["patient_id"]
    )

@router.get("/history/{session_id}", response_model=ConversationResponse)
def get_history(session_id: str, db: Session = Depends(get_db)):
    conv_repo = ConversationRepository(db)
    msg_repo = MessageRepository(db)
    
    conversation = conv_repo.get_by_session_id(session_id)
    if not conversation:
        return ConversationResponse(
            session_id=session_id,
            patient_id=None,
            messages=[]
        )
        
    messages = msg_repo.get_last_n_messages(conversation.conversation_id, limit=20)
    
    return ConversationResponse(
        session_id=conversation.session_id,
        patient_id=conversation.patient_id,
        messages=messages
    )
