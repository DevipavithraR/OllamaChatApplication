import re
import json
import logging
from sqlalchemy.orm import Session
from app.services.CustomerService import CustomerService
from app.services.BookingService import BookingService
from app.repositories.ConversationRepository import ConversationRepository
from app.schemas.customer_schema import CustomerCreate
from app.schemas.booking_schema import BookingCreateWithCustomer, BookingUpdate

logger = logging.getLogger("app.services.ActionInterceptor")

class ActionInterceptor:
    def __init__(self, db: Session):
        self.db = db
        self.customer_service = CustomerService(db)
        self.booking_service = BookingService(db)
        self.conversation_repo = ConversationRepository(db)

    def intercept_actions(self, conversation_id: int, response_text: str) -> str:
        cleaned_text = response_text

        # 1. CUSTOMER_IDENTIFY
        ident_pattern = r"```CUSTOMER_IDENTIFY:\s*(\{.*?\})\s*```"
        ident_match = re.search(ident_pattern, response_text, re.DOTALL)
        if ident_match:
            json_str = ident_match.group(1)
            try:
                data = json.loads(json_str)
                name = data.get("name")
                phone = data.get("phone")
                if name and phone:
                    customer = self.customer_service.get_customer_by_phone(phone)
                    if not customer:
                        customer = self.customer_service.create_customer(
                            CustomerCreate(name=name, phone_number=phone)
                        )
                    self.conversation_repo.link_customer(conversation_id, customer.customer_id)
                    logger.info(f"Linked conversation {conversation_id} to customer {customer.customer_id}")
            except Exception as e:
                logger.error(f"Failed to process CUSTOMER_IDENTIFY: {str(e)}")
            cleaned_text = re.sub(ident_pattern, "", cleaned_text, flags=re.DOTALL).strip()

        # 2. MOVIE_BOOKING_CONFIRM
        confirm_pattern = r"```MOVIE_BOOKING_CONFIRM:\s*(\{.*?\})\s*```"
        confirm_match = re.search(confirm_pattern, response_text, re.DOTALL)
        if confirm_match:
            json_str = confirm_match.group(1)
            try:
                data = json.loads(json_str)
                name = data.get("name")
                phone = data.get("phone")
                show_id = data.get("show_id")
                seat_numbers = data.get("seat_numbers")
                number_of_tickets = data.get("number_of_tickets")
                if name and phone and show_id and seat_numbers and number_of_tickets:
                    dto = BookingCreateWithCustomer(
                        name=name,
                        phone=phone,
                        show_id=int(show_id),
                        seat_numbers=seat_numbers,
                        number_of_tickets=int(number_of_tickets)
                    )
                    booking = self.booking_service.create_booking_with_customer(dto)
                    self.conversation_repo.link_customer(conversation_id, booking.customer_id)
                    logger.info(f"Booked tickets: Booking ID {booking.booking_id} for customer {booking.customer_id}")
            except Exception as e:
                logger.error(f"Failed to process MOVIE_BOOKING_CONFIRM: {str(e)}")
            cleaned_text = re.sub(confirm_pattern, "", cleaned_text, flags=re.DOTALL).strip()

        # 3. BOOKING_CANCEL
        cancel_pattern = r"```BOOKING_CANCEL:\s*(\{.*?\})\s*```"
        cancel_match = re.search(cancel_pattern, response_text, re.DOTALL)
        if cancel_match:
            json_str = cancel_match.group(1)
            try:
                data = json.loads(json_str)
                booking_id = data.get("booking_id")
                if booking_id:
                    self.booking_service.cancel_booking(int(booking_id))
                    logger.info(f"Cancelled booking {booking_id}")
            except Exception as e:
                logger.error(f"Failed to process BOOKING_CANCEL: {str(e)}")
            cleaned_text = re.sub(cancel_pattern, "", cleaned_text, flags=re.DOTALL).strip()

        # 4. BOOKING_MODIFY
        modify_pattern = r"```BOOKING_MODIFY:\s*(\{.*?\})\s*```"
        modify_match = re.search(modify_pattern, response_text, re.DOTALL)
        if modify_match:
            json_str = modify_match.group(1)
            try:
                data = json.loads(json_str)
                booking_id = data.get("booking_id")
                seat_numbers = data.get("seat_numbers")
                number_of_tickets = data.get("number_of_tickets")
                if booking_id:
                    update_schema = BookingUpdate(
                        seat_numbers=seat_numbers,
                        number_of_tickets=int(number_of_tickets) if number_of_tickets is not None else None
                    )
                    self.booking_service.update_booking(int(booking_id), update_schema)
                    logger.info(f"Modified booking {booking_id}")
            except Exception as e:
                logger.error(f"Failed to process BOOKING_MODIFY: {str(e)}")
            cleaned_text = re.sub(modify_pattern, "", cleaned_text, flags=re.DOTALL).strip()

        return cleaned_text
