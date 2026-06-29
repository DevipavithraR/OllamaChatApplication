from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from app.repositories.ConversationRepository import ConversationRepository
from app.services.CustomerService import CustomerService
from app.services.VehicleService import VehicleService
from app.services.BookingService import BookingService
from app.services.ServiceSearchService import ServiceSearchService
from app.services.PromptBuilder import PromptBuilder
from app.services.OllamaService import OllamaService
from app.services.ActionInterceptor import ActionInterceptor
from app.models.Conversation import Conversation
import logging

logger = logging.getLogger("app.services.ChatService")

class ChatService:
    def __init__(self, db: Session):
        self.db = db
        self.conversation_repo = ConversationRepository(db)
        self.customer_service = CustomerService(db)
        self.vehicle_service = VehicleService(db)
        self.booking_service = BookingService(db)
        self.search_service = ServiceSearchService(db)
        self.ollama_service = OllamaService()
        self.interceptor = ActionInterceptor(db)

    def process_message(self, session_id: str, user_message: str) -> Dict[str, Any]:
        """
        Processes a chat message: Retrieves history, executes RAG, compiles prompt, calls Ollama,
        intercepts actions, persists messages, and returns final payload.
        """
        # 1. Fetch or create conversation
        conversation = self.conversation_repo.get_by_session_id(session_id)
        if not conversation:
            logger.info(f"Conversation session '{session_id}' not found. Creating new...")
            conversation = Conversation(session_id=session_id)
            conversation = self.conversation_repo.create(conversation)

        # Retrieve last 10 messages for context
        history_messages = self.conversation_repo.get_last_n_messages(conversation.conversation_id, limit=10)

        # 2. RAG search
        services = self.search_service.search_services(user_message)
        mechanics = self.search_service.search_mechanics(user_message)

        # Fallback to general listing if keywords check matching user intent but empty search
        msg_lower = user_message.lower()
        if not services and any(kw in msg_lower for kw in ["service", "package", "cost", "price", "duration", "offer"]):
            services = self.search_service.get_all_services()[:5]

        if not mechanics and any(kw in msg_lower for kw in ["mechanic", "expert", "specialist", "experience", "staff"]):
            mechanics = self.search_service.get_all_mechanics()[:5]

        # Customer-specific context
        customer = None
        vehicles = []
        bookings = []
        
        if conversation.customer_id:
            try:
                customer = self.customer_service.get_customer_by_id(conversation.customer_id)
                vehicles = self.vehicle_service.get_vehicles_by_customer(customer.customer_id)
                bookings = self.booking_service.repository.get_by_customer_id(customer.customer_id)
            except Exception as e:
                logger.error(f"Error loading customer contexts: {str(e)}")

        # 3. Compile System Prompt
        system_prompt = PromptBuilder.build_system_prompt(
            services=services,
            mechanics=mechanics,
            customer=customer,
            vehicles=vehicles,
            bookings=bookings
        )

        # 4. Compile Messages
        ollama_messages = [{"role": "system", "content": system_prompt}]
        for msg in history_messages:
            role = "user" if msg.sender == "user" else "assistant"
            ollama_messages.append({"role": role, "content": msg.message})
        
        ollama_messages.append({"role": "user", "content": user_message})

        # Save user message to database
        self.conversation_repo.add_message(conversation.conversation_id, sender="user", content=user_message)

        # 5. Query Ollama
        bot_response = self.ollama_service.chat(ollama_messages)

        # 6. Intercept Structured Actions
        bot_response, linked_customer_id = self.interceptor.intercept_and_execute(
            conversation.conversation_id,
            bot_response
        )

        # Save bot response to database
        self.conversation_repo.add_message(conversation.conversation_id, sender="bot", content=bot_response)

        # Fetch latest customer linkage status
        self.db.refresh(conversation)

        return {
            "session_id": session_id,
            "response": bot_response,
            "customer_id": conversation.customer_id
        }
