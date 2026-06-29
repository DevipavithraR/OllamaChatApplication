import logging
from datetime import datetime
from typing import Dict, Any
from sqlalchemy.orm import Session
from app.repositories.ConversationRepository import ConversationRepository
from app.services.CustomerService import CustomerService
from app.services.MovieSearchService import MovieSearchService
from app.services.BookingService import BookingService
from app.services.ollama import OllamaService
from app.services.PromptBuilder import PromptBuilder
from app.services.ActionInterceptor import ActionInterceptor

logger = logging.getLogger("app.services.chatbot")

class ChatbotService:
    def __init__(self, db: Session):
        self.db = db
        self.conversation_repo = ConversationRepository(db)
        self.customer_service = CustomerService(db)
        self.movie_search_service = MovieSearchService(db)
        self.booking_service = BookingService(db)
        self.ollama_service = OllamaService()
        self.action_interceptor = ActionInterceptor(db)

    def process_message(self, session_id: str, user_message: str) -> Dict[str, Any]:
        """
        Process an incoming chat message:
        1. Fetch or create conversation history.
        2. Perform RAG query on movies, theatres, shows, and bookings.
        3. Build system prompt context.
        4. Send context + history + new message to Ollama.
        5. Intercept and parse special action tags.
        6. Persist messages and return response.
        """
        # 1. Fetch or create conversation
        conversation = self.conversation_repo.get_by_session_id(session_id)
        if not conversation:
            from app.models.conversation import Conversation
            conversation = Conversation(session_id=session_id)
            conversation = self.conversation_repo.create(conversation)

        # Retrieve last 10 messages for context
        history_messages = self.conversation_repo.get_last_n_messages(conversation.conversation_id, limit=10)

        # 2. RAG Context generation
        theatres = self.movie_search_service.get_all_theatres()
        theatres_context = "\n".join([
            f"- {t.theatre_name} located at {t.location} ({t.screens} screens)"
            for t in theatres
        ]) if theatres else "No theatres registered."

        shows = self.movie_search_service.get_all_shows()
        shows_context = "\n".join([
            f"- Show ID {s.show_id}: \"{s.movie.title}\" (Genre: {s.movie.genre}, Language: {s.movie.language}, Rating: {s.movie.rating}) at {s.theatre.theatre_name} (Screen {s.screen_number}) on {s.show_datetime.strftime('%Y-%m-%d %H:%M:%S')} - ${s.ticket_price} ({s.available_seats}/{s.total_seats} seats available)"
            for s in shows
        ]) if shows else "No shows scheduled."

        customer_context = "Anonymous Customer"
        bookings_context = "No bookings found."

        if conversation.customer_id:
            customer = self.customer_service.get_customer_by_id(conversation.customer_id)
            customer_context = f"Identified Customer: {customer.name} (Phone: {customer.phone_number}, Email: {customer.email or 'N/A'})"
            
            bookings = self.booking_service.get_bookings_by_customer(customer.customer_id)
            if bookings:
                bookings_context = "\n".join([
                    f"- Booking ID {b.booking_id}: {b.number_of_tickets} tickets for \"{b.show.movie.title}\" at {b.show.theatre.theatre_name} (Seats: {b.seat_numbers}) [Status: {b.booking_status}]"
                    for b in bookings
                ])
            else:
                bookings_context = "No booking history found for this customer."

        # 3. Build prompt
        current_time = datetime.now()
        system_prompt = PromptBuilder.build_system_prompt(
            current_time=current_time,
            shows_context=shows_context,
            theatres_context=theatres_context,
            customer_context=customer_context,
            bookings_context=bookings_context
        )

        # Build message history payload for Ollama
        ollama_messages = [{"role": "system", "content": system_prompt}]
        for msg in history_messages:
            ollama_messages.append({"role": "user" if msg.sender == "user" else "assistant", "content": msg.message})
        
        # Append current user message
        ollama_messages.append({"role": "user", "content": user_message})

        # Save user message to DB
        self.conversation_repo.add_message(conversation.conversation_id, sender="user", content=user_message)

        # 4. Call Ollama Service
        bot_response = self.ollama_service.chat(ollama_messages)

        # 5. Parse action tags from bot response
        bot_response = self.action_interceptor.intercept_actions(conversation.conversation_id, bot_response)

        # Save bot response to DB
        self.conversation_repo.add_message(conversation.conversation_id, sender="bot", content=bot_response)

        # Reload conversation to see if customer_id was updated during action processing
        self.db.refresh(conversation)

        return {
            "session_id": session_id,
            "response": bot_response,
            "customer_id": conversation.customer_id
        }
