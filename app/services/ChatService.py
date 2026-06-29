from sqlalchemy.orm import Session
from datetime import datetime
from typing import Dict, Any
import logging
from app.repositories.ConversationRepository import ConversationRepository
from app.services.MemberService import MemberService
from app.services.MembershipService import MembershipService
from app.services.TrainerSearchService import TrainerSearchService
from app.services.OllamaService import OllamaService
from app.services.PromptBuilder import PromptBuilder
from app.services.ActionInterceptor import ActionInterceptor
from app.models.Conversation import Conversation

logger = logging.getLogger("app.services.ChatService")

class ChatService:
    def __init__(self, db: Session):
        self.db = db
        self.conversation_repo = ConversationRepository(db)
        self.member_service = MemberService(db)
        self.membership_service = MembershipService(db)
        self.trainer_service = TrainerSearchService(db)
        self.ollama_service = OllamaService()
        self.action_interceptor = ActionInterceptor(db)

    def process_message(self, session_id: str, user_message: str) -> Dict[str, Any]:
        # 1. Fetch or create conversation
        conversation = self.conversation_repo.get_by_session_id(session_id)
        if not conversation:
            conversation = Conversation(session_id=session_id)
            conversation = self.conversation_repo.create(conversation)

        # Retrieve last 10 messages for context
        history_messages = self.conversation_repo.get_last_n_messages(conversation.conversation_id, limit=10)

        # Save user message to DB
        self.conversation_repo.add_message(conversation.conversation_id, sender="user", content=user_message)

        # 2. RAG: Retrieve plans and trainers
        # Check if the user is asking about plans
        plans = []
        if any(word in user_message.lower() for word in ["plan", "membership", "price", "fee", "cost", "gold", "silver", "platinum", "benefit", "duration"]):
            plans = self.membership_service.get_all_plans()
        else:
            plans = self.membership_service.search_plans(user_message)
            if not plans:
                plans = self.membership_service.get_all_plans()[:5]

        # Check if the user is asking about trainers
        trainers = []
        if any(word in user_message.lower() for word in ["trainer", "coach", "book", "session", "schedule", "specialization", "experience", "availability", "time", "day", "rahul", "priya", "vikram"]):
            trainers = self.trainer_service.get_all_trainers()
        else:
            trainers = self.trainer_service.search_trainers(user_message)
            if not trainers:
                trainers = self.trainer_service.get_all_trainers()[:5]

        # Member details and bookings
        member = None
        bookings = []
        if conversation.member_id:
            member = self.member_service.get_member_by_id(conversation.member_id)
            if member:
                bookings = self.trainer_service.booking_repository.get_upcoming_bookings_for_member(member.member_id)

        # 3. Build System Prompt Context
        current_time = datetime.now()
        system_prompt = PromptBuilder.build_system_prompt(
            current_time=current_time,
            plans=plans,
            trainers=trainers,
            member=member,
            bookings=bookings
        )

        # Build message history payload for Ollama
        ollama_messages = [{"role": "system", "content": system_prompt}]
        for msg in history_messages:
            ollama_messages.append({
                "role": "user" if msg.sender == "user" else "assistant",
                "content": msg.message
            })
        
        # Append current user message
        ollama_messages.append({"role": "user", "content": user_message})

        # 4. Call Ollama
        bot_response = self.ollama_service.chat(ollama_messages)

        # 5. Intercept Actions
        bot_response = self.action_interceptor.intercept_and_execute(conversation.conversation_id, bot_response)

        # Save bot response to DB
        self.conversation_repo.add_message(conversation.conversation_id, sender="bot", content=bot_response)

        # Refresh conversation to get any updated member_id
        self.db.refresh(conversation)

        return {
            "session_id": session_id,
            "response": bot_response,
            "member_id": conversation.member_id
        }
