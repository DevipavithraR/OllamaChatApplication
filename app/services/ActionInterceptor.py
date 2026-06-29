import json
import re
import logging
from datetime import datetime, date
from typing import Tuple, Optional
from sqlalchemy.orm import Session

from app.repositories.ConversationRepository import ConversationRepository
from app.services.MemberService import MemberService
from app.services.BookSearchService import BookSearchService
from app.services.LibraryService import LibraryService
from app.schemas.member_schema import MemberCreate
from app.schemas.issued_book_schema import IssuedBookCreate

logger = logging.getLogger("app.services.ActionInterceptor")

class ActionInterceptor:
    def __init__(self, db: Session):
        self.db = db
        self.conversation_repo = ConversationRepository(db)
        self.member_service = MemberService(db)
        self.book_service = BookSearchService(db)
        self.library_service = LibraryService(db)

    def intercept_actions(self, conversation_id: int, response_text: str) -> Tuple[str, Optional[int]]:
        """
        Intercepts structured output tags (MEMBER_IDENTIFY, BOOK_ISSUE, BOOK_RETURN, DUE_DATE_CHECK),
        processes them against the database, strips the tags, and returns the cleaned text and any associated member_id.
        """
        cleaned_text = response_text
        member_id = None

        # 1. Intercept MEMBER_IDENTIFY
        ident_pattern = r"```MEMBER_IDENTIFY\s*(\{.*?\})\s*```"
        ident_match = re.search(ident_pattern, response_text, re.DOTALL)
        if ident_match:
            json_str = ident_match.group(1)
            try:
                data = json.loads(json_str)
                name = data.get("name")
                phone = data.get("phone")
                if name and phone:
                    # Lookup or create member
                    member = self.member_service.get_member_by_phone(phone)
                    if not member:
                        logger.info(f"Registering new member on identification: {name} ({phone})")
                        member = self.member_service.create_member(
                            MemberCreate(name=name, phone_number=phone)
                        )
                    
                    member_id = member.member_id
                    self.conversation_repo.link_member(conversation_id, member_id)
                    logger.info(f"Linked conversation {conversation_id} to member {member_id}")
            except Exception as e:
                logger.error(f"Error intercepting MEMBER_IDENTIFY: {str(e)}")
            cleaned_text = re.sub(ident_pattern, "", cleaned_text, flags=re.DOTALL).strip()

        # 2. Intercept BOOK_ISSUE
        issue_pattern = r"```BOOK_ISSUE\s*(\{.*?\})\s*```"
        issue_match = re.search(issue_pattern, response_text, re.DOTALL)
        if issue_match:
            json_str = issue_match.group(1)
            try:
                data = json.loads(json_str)
                name = data.get("name")
                phone = data.get("phone")
                book_title = data.get("book_title")
                issue_date_str = data.get("issue_date")
                due_date_str = data.get("due_date")

                if name and phone and book_title:
                    # Lookup or create member
                    member = self.member_service.get_member_by_phone(phone)
                    if not member:
                        logger.info(f"Registering member on book issue: {name} ({phone})")
                        member = self.member_service.create_member(
                            MemberCreate(name=name, phone_number=phone)
                        )
                    member_id = member.member_id
                    self.conversation_repo.link_member(conversation_id, member_id)

                    # Lookup book
                    book = self.book_service.get_book_by_title(book_title)
                    if not book:
                        # Try partial search
                        books = self.book_service.search_books(book_title)
                        if books:
                            book = books[0]

                    if book:
                        # Parse dates
                        try:
                            issue_date_val = datetime.strptime(issue_date_str, "%Y-%m-%d").date() if issue_date_str else date.today()
                            due_date_val = datetime.strptime(due_date_str, "%Y-%m-%d").date()
                        except Exception:
                            # Fallback if parsing fails
                            issue_date_val = date.today()
                            due_date_val = date.fromordinal(date.today().toordinal() + 14)

                        logger.info(f"Issuing book '{book.title}' to member '{member.name}'")
                        self.library_service.issue_book(
                            IssuedBookCreate(
                                member_id=member.member_id,
                                book_id=book.book_id,
                                issue_date=issue_date_val,
                                due_date=due_date_val
                            )
                        )
                    else:
                        logger.warning(f"Book issue failed: Book '{book_title}' not found in database.")
            except Exception as e:
                logger.error(f"Error intercepting BOOK_ISSUE: {str(e)}")
            cleaned_text = re.sub(issue_pattern, "", cleaned_text, flags=re.DOTALL).strip()

        # 3. Intercept BOOK_RETURN
        return_pattern = r"```BOOK_RETURN\s*(\{.*?\})\s*```"
        return_match = re.search(return_pattern, response_text, re.DOTALL)
        if return_match:
            json_str = return_match.group(1)
            try:
                data = json.loads(json_str)
                issue_id = data.get("issue_id")
                if issue_id:
                    logger.info(f"Returning book for issue record: {issue_id}")
                    self.library_service.return_book(int(issue_id))
            except Exception as e:
                logger.error(f"Error intercepting BOOK_RETURN: {str(e)}")
            cleaned_text = re.sub(return_pattern, "", cleaned_text, flags=re.DOTALL).strip()

        # 4. Intercept DUE_DATE_CHECK
        due_pattern = r"```DUE_DATE_CHECK\s*(\{.*?\})\s*```"
        due_match = re.search(due_pattern, response_text, re.DOTALL)
        if due_match:
            json_str = due_match.group(1)
            try:
                data = json.loads(json_str)
                issue_id = data.get("issue_id")
                if issue_id:
                    logger.info(f"Checking due date for issue record: {issue_id}")
                    self.library_service.get_due_date_info(int(issue_id))
            except Exception as e:
                logger.error(f"Error intercepting DUE_DATE_CHECK: {str(e)}")
            cleaned_text = re.sub(due_pattern, "", cleaned_text, flags=re.DOTALL).strip()

        return cleaned_text, member_id
