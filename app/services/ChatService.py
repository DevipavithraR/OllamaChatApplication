import logging
from typing import Dict, Any, List
from sqlalchemy.orm import Session

from app.repositories.ConversationRepository import ConversationRepository
from app.repositories.MessageRepository import MessageRepository
from app.services.BookSearchService import BookSearchService
from app.services.MemberService import MemberService
from app.services.LibraryService import LibraryService
from app.services.OllamaService import OllamaService
from app.services.PromptBuilder import PromptBuilder
from app.services.ActionInterceptor import ActionInterceptor
from app.models.conversation import Conversation

logger = logging.getLogger("app.services.ChatService")

class ChatService:
    def __init__(self, db: Session):
        self.db = db
        self.conversation_repo = ConversationRepository(db)
        self.message_repo = MessageRepository(db)
        self.book_service = BookSearchService(db)
        self.member_service = MemberService(db)
        self.library_service = LibraryService(db)
        self.ollama_service = OllamaService()
        self.prompt_builder = PromptBuilder()
        self.action_interceptor = ActionInterceptor(db)

    def get_or_create_conversation(self, session_id: str) -> Conversation:
        conversation = self.conversation_repo.get_by_session_id(session_id)
        if not conversation:
            conversation = Conversation(session_id=session_id)
            conversation = self.conversation_repo.create(conversation)
        return conversation

    def get_conversation_history(self, session_id: str) -> Conversation:
        return self.get_or_create_conversation(session_id)

    def process_message(self, session_id: str, user_message: str) -> Dict[str, Any]:
        """
        Main chat pipeline orchestration.
        """
        # 1. Retrieve or create conversation
        conversation = self.get_or_create_conversation(session_id)
        conversation_id = conversation.conversation_id

        # 2. Add user message to DB
        self.message_repo.add_message(conversation_id, sender="user", message_text=user_message)

        # 3. Retrieve history messages (last 10)
        history_messages = self.message_repo.get_last_n_messages(conversation_id, limit=10)

        # 4. Search Books Context (RAG)
        # Search dynamically matching the user's message
        books = self.book_service.search_books(user_message)
        
        # If no specific matches and user is talking about books generally, inject first 5 books
        if not books and any(w in user_message.lower() for w in ["book", "library", "author", "read", "borrow", "catalog", "find", "search"]):
            books = self.book_service.get_all_books(limit=5)

        # 5. Retrieve Member & Issued Book Contexts
        member = None
        issued_records = []
        if conversation.member_id:
            try:
                member = self.member_service.get_member_by_id(conversation.member_id)
                issued_records = self.library_service.get_borrowing_history(member.member_id)
            except Exception as e:
                logger.warning(f"Error fetching member context: {str(e)}")

        # 6. Build Prompt
        system_prompt = self.prompt_builder.build_system_prompt(
            books=books,
            member=member,
            issued_records=issued_records
        )

        # Build message history for Ollama
        ollama_messages = [{"role": "system", "content": system_prompt}]
        for msg in history_messages:
            ollama_messages.append({
                "role": "user" if msg.sender == "user" else "assistant",
                "content": msg.message
            })

        # Append current user message
        ollama_messages.append({"role": "user", "content": user_message})

        # 7. Call Ollama Service
        bot_raw_response = self.ollama_service.chat(ollama_messages)

        # 8. Intercept Action Tags
        cleaned_response, updated_member_id = self.action_interceptor.intercept_actions(
            conversation_id, bot_raw_response
        )

        # 9. Save bot response to DB
        self.message_repo.add_message(conversation_id, sender="bot", message_text=cleaned_response)

        # Refresh conversation to get updated member link
        self.db.refresh(conversation)

        return {
            "session_id": session_id,
            "response": cleaned_response,
            "member_id": conversation.member_id,
            "customer_id": conversation.member_id # backwards-compatible with old frontend references
        }
