import json
import re
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from app.config import settings
from app.repositories.conversation import ConversationRepository
from app.services.customer import CustomerService
from app.services.reservation import ReservationService
from app.services.menu import MenuService
from app.services.ollama import OllamaService
from app.schemas.reservation import ReservationCreateWithCustomer

logger = logging.getLogger("app.services.chatbot")

class ChatbotService:
    def __init__(self, db: Session):
        self.db = db
        self.conversation_repo = ConversationRepository(db)
        self.customer_service = CustomerService(db)
        self.reservation_service = ReservationService(db)
        self.menu_service = MenuService(db)
        self.ollama_service = OllamaService()

    def process_message(self, session_id: str, user_message: str) -> Dict[str, Any]:
        """
        Process an incoming chat message:
        1. Fetch or create conversation history.
        2. Perform RAG query on menu and reservations.
        3. Build system prompt context.
        4. Send context + history + new message to Ollama.
        5. Intercept and parse special action tags (e.g., booking table, identifying customer).
        6. Persist messages and return response.
        """
        # 1. Fetch or create conversation
        conversation = self.conversation_repo.get_by_session_id(session_id)
        if not conversation:
            from app.models.conversation import Conversation
            conversation = Conversation(session_id=session_id)
            conversation = self.conversation_repo.create(conversation)

        # Retrieve last 10 messages for context
        history_messages = self.conversation_repo.get_last_n_messages(conversation.id, limit=10)

        # 2. RAG: Search menu items based on the user's current message
        menu_items = self.menu_service.search_menu_items(user_message)
        # If no specific matches, get general available menu to allow general questions
        if not menu_items and any(word in user_message.lower() for word in ["menu", "food", "eat", "drink", "dish", "special", "price"]):
            menu_items = self.menu_service.get_available_menu_items()[:8]

        menu_context = ""
        if menu_items:
            menu_context = "\n".join([
                f"- {item.name} ({item.category}): {item.description} - ${item.price}"
                for item in menu_items
            ])
        else:
            menu_context = "No specific menu items matched. Assure the customer we have a premium Italian menu available upon request."

        # RAG: Customer & Reservation context
        customer_context = "Anonymous Customer"
        reservation_context = "No reservation details available."
        
        if conversation.customer_id:
            customer = self.customer_service.get_customer_by_id(conversation.customer_id)
            customer_context = f"Identified Customer: {customer.name} (Phone: {customer.phone}, Email: {customer.email or 'N/A'})"
            
            # Fetch upcoming reservations
            reservations = self.reservation_service.repository.get_upcoming_reservations_for_customer(customer.id)
            if reservations:
                reservation_context = "\n".join([
                    f"- Reservation ID {res.id}: {res.reservation_time.strftime('%Y-%m-%d %H:%M:%S')} for {res.party_size} guests [Status: {res.status}] (Requests: {res.special_requests or 'None'})"
                    for res in reservations
                ])
            else:
                reservation_context = "No upcoming active reservations found for this customer."

        # 3. Build System Prompt Context
        current_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        system_prompt = f"""You are the AI Receptionist for "Bella Italia", a premium Italian restaurant.
Your goal is to answer customer questions about the menu, check existing reservations, and book new reservations.

CRITICAL INSTRUCTIONS (No Hallucination Policy):
1. You MUST ONLY answer questions about menu items using the provided "Menu Context" below. If a dish or beverage is not in the context, state politely that we do not serve it. Do not make up items, descriptions, or prices.
2. If the user asks about an existing reservation, only use the "Reservation Context" below.
3. Keep your answers concise, friendly, and professional.
4. Assume the current date and time is: {current_time_str}.

Menu Context:
{menu_context}

Customer Context:
{customer_context}

Reservation Context:
{reservation_context}

Booking & Identification Instructions:
- To book a table, you need: Full Name, Phone Number, Date and Time of reservation, and Party Size.
- If details are missing, ask the user for them.
- Once you have gathered ALL 4 details, you MUST append a JSON block at the very end of your response inside triple backticks with the prefix `RESERVATION_CONFIRM:` (and nothing else in that block).
Format:
```RESERVATION_CONFIRM:
{{
  "name": "Customer Name",
  "phone": "Phone Number",
  "datetime": "YYYY-MM-DD HH:MM:SS",
  "party_size": 4,
  "special_requests": "Any special instructions or null"
}}
```
- If the user simply identifies themselves (e.g. "I am John Doe, my phone is +1234567890") to inquire about reservations or log in, append:
```CUSTOMER_IDENTIFY:
{{
  "name": "Customer Name",
  "phone": "Phone Number"
}}
```
Do not output these blocks until you have verified the details. Convert relative dates (e.g. "tomorrow at 7 PM") into absolute YYYY-MM-DD HH:MM:SS format using the current time context ({current_time_str}).
"""

        # Build message history payload for Ollama
        ollama_messages = [{"role": "system", "content": system_prompt}]
        for msg in history_messages:
            ollama_messages.append({"role": "user" if msg.sender == "user" else "assistant", "content": msg.content})
        
        # Append current user message
        ollama_messages.append({"role": "user", "content": user_message})

        # Save user message to DB
        self.conversation_repo.add_message(conversation.id, sender="user", content=user_message)

        # 4. Call Ollama Service
        bot_response = self.ollama_service.chat(ollama_messages)

        # 5. Parse action tags from bot response
        bot_response = self._handle_actions(conversation.id, bot_response)

        # Save bot response to DB
        self.conversation_repo.add_message(conversation.id, sender="bot", content=bot_response)

        # Reload conversation to see if customer_id was updated during action processing
        self.db.refresh(conversation)

        return {
            "session_id": session_id,
            "response": bot_response,
            "customer_id": conversation.customer_id
        }

    def _handle_actions(self, conversation_id: int, response_text: str) -> str:
        """
        Detects, extracts, and handles RESERVATION_CONFIRM and CUSTOMER_IDENTIFY action blocks.
        Strips the blocks from the final response text.
        """
        cleaned_text = response_text

        # Pattern for RESERVATION_CONFIRM
        res_pattern = r"```RESERVATION_CONFIRM:\s*(\{.*?\})\s*```"
        res_match = re.search(res_pattern, response_text, re.DOTALL)
        if res_match:
            json_str = res_match.group(1)
            try:
                data = json.loads(json_str)
                logger.info(f"Processing automatic reservation booking: {data}")
                
                # Check formatting of datetime
                res_time = datetime.strptime(data["datetime"], "%Y-%m-%d %H:%M:%S")
                
                dto = ReservationCreateWithCustomer(
                    customer_name=data["name"],
                    customer_phone=data["phone"],
                    customer_email=data.get("email"),
                    reservation_time=res_time,
                    party_size=int(data["party_size"]),
                    special_requests=data.get("special_requests"),
                    status="CONFIRMED"
                )
                # Run reservation logic
                reservation = self.reservation_service.create_reservation_with_customer(dto)
                # Link conversation to the customer
                self.conversation_repo.link_customer(conversation_id, reservation.customer_id)
                logger.info(f"Successfully booked reservation {reservation.id} for customer {reservation.customer_id}")
            except Exception as e:
                logger.error(f"Failed to process reservation confirm block: {str(e)}")
            
            # Strip the block from the response
            cleaned_text = re.sub(res_pattern, "", cleaned_text, flags=re.DOTALL).strip()

        # Pattern for CUSTOMER_IDENTIFY
        ident_pattern = r"```CUSTOMER_IDENTIFY:\s*(\{.*?\})\s*```"
        ident_match = re.search(ident_pattern, response_text, re.DOTALL)
        if ident_match:
            json_str = ident_match.group(1)
            try:
                data = json.loads(json_str)
                logger.info(f"Processing customer identification: {data}")
                
                # Lookup or create customer
                phone = data["phone"]
                name = data["name"]
                customer = self.customer_service.get_customer_by_phone(phone)
                if not customer:
                    from app.schemas.customer import CustomerCreate
                    customer = self.customer_service.create_customer(CustomerCreate(name=name, phone=phone))
                
                self.conversation_repo.link_customer(conversation_id, customer.id)
                logger.info(f"Linked conversation {conversation_id} to customer {customer.id}")
            except Exception as e:
                logger.error(f"Failed to process customer identify block: {str(e)}")
                
            cleaned_text = re.sub(ident_pattern, "", cleaned_text, flags=re.DOTALL).strip()

        return cleaned_text
