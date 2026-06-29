import re
import json
import logging
from datetime import datetime
from sqlalchemy.orm import Session
from app.repositories.ConversationRepository import ConversationRepository
from app.services.MemberService import MemberService
from app.services.MembershipService import MembershipService
from app.services.TrainerSearchService import TrainerSearchService
from app.schemas.member_schema import MemberCreate
from app.schemas.trainer_booking_schema import TrainerBookingCreate

logger = logging.getLogger("app.services.ActionInterceptor")

class ActionInterceptor:
    def __init__(self, db: Session):
        self.db = db
        self.conversation_repo = ConversationRepository(db)
        self.member_service = MemberService(db)
        self.membership_service = MembershipService(db)
        self.trainer_service = TrainerSearchService(db)

    def intercept_and_execute(self, conversation_id: int, response_text: str) -> str:
        cleaned_text = response_text

        # 1. MEMBER_IDENTIFY
        ident_pattern = r"```MEMBER_IDENTIFY\s*(\{.*?\})\s*```"
        ident_match = re.search(ident_pattern, response_text, re.DOTALL)
        if ident_match:
            json_str = ident_match.group(1)
            try:
                data = json.loads(json_str)
                name = data.get("name")
                phone = data.get("phone")
                
                member = self.member_service.get_member_by_phone(phone)
                if not member:
                    dto = MemberCreate(name=name, phone_number=phone)
                    member = self.member_service.create_member(dto)
                
                self.conversation_repo.link_member(conversation_id, member.member_id)
                logger.info(f"MEMBER_IDENTIFY: Linked conversation {conversation_id} to member {member.member_id}")
            except Exception as e:
                logger.error(f"Failed to process MEMBER_IDENTIFY: {str(e)}")
            
            cleaned_text = re.sub(ident_pattern, "", cleaned_text, flags=re.DOTALL).strip()

        # 2. MEMBERSHIP_REGISTER
        reg_pattern = r"```MEMBERSHIP_REGISTER\s*(\{.*?\})\s*```"
        reg_match = re.search(reg_pattern, response_text, re.DOTALL)
        if reg_match:
            json_str = reg_match.group(1)
            try:
                data = json.loads(json_str)
                name = data.get("name")
                phone = data.get("phone")
                email = data.get("email")
                age = int(data.get("age", 0))
                
                member = self.member_service.get_member_by_phone(phone)
                if member:
                    member.membership_status = "ACTIVE"
                    member.email = email
                    member.age = age
                    member.name = name
                    self.db.commit()
                else:
                    dto = MemberCreate(
                        name=name,
                        phone_number=phone,
                        email=email,
                        age=age,
                        membership_status="ACTIVE"
                    )
                    member = self.member_service.create_member(dto)
                
                self.conversation_repo.link_member(conversation_id, member.member_id)
                logger.info(f"MEMBERSHIP_REGISTER: Registered and linked member {member.member_id}")
            except Exception as e:
                logger.error(f"Failed to process MEMBERSHIP_REGISTER: {str(e)}")
                
            cleaned_text = re.sub(reg_pattern, "", cleaned_text, flags=re.DOTALL).strip()

        # 3. TRAINER_BOOKING_CONFIRM
        book_pattern = r"```TRAINER_BOOKING_CONFIRM\s*(\{.*?\})\s*```"
        book_match = re.search(book_pattern, response_text, re.DOTALL)
        if book_match:
            json_str = book_match.group(1)
            try:
                data = json.loads(json_str)
                member_name = data.get("member_name")
                phone = data.get("phone")
                trainer_name = data.get("trainer_name")
                booking_datetime_str = data.get("booking_datetime")
                training_goal = data.get("training_goal")
                
                member = self.member_service.get_member_by_phone(phone)
                if not member:
                    dto = MemberCreate(name=member_name, phone_number=phone)
                    member = self.member_service.create_member(dto)
                
                self.conversation_repo.link_member(conversation_id, member.member_id)
                
                trainer = self.trainer_service.get_trainer_by_name(trainer_name)
                if trainer:
                    booking_datetime = datetime.strptime(booking_datetime_str, "%Y-%m-%d %H:%M:%S")
                    booking_dto = TrainerBookingCreate(
                        member_id=member.member_id,
                        trainer_id=trainer.trainer_id,
                        booking_datetime=booking_datetime,
                        status="CONFIRMED",
                        training_goal=training_goal
                    )
                    booking = self.trainer_service.create_booking(booking_dto)
                    logger.info(f"TRAINER_BOOKING_CONFIRM: Booked {booking.booking_id} for member {member.member_id}")
                else:
                    logger.error(f"Trainer '{trainer_name}' not found during booking.")
            except Exception as e:
                logger.error(f"Failed to process TRAINER_BOOKING_CONFIRM: {str(e)}")
                
            cleaned_text = re.sub(book_pattern, "", cleaned_text, flags=re.DOTALL).strip()

        # 4. TRAINER_BOOKING_CANCEL
        cancel_pattern = r"```TRAINER_BOOKING_CANCEL\s*(\{.*?\})\s*```"
        cancel_match = re.search(cancel_pattern, response_text, re.DOTALL)
        if cancel_match:
            json_str = cancel_match.group(1)
            try:
                data = json.loads(json_str)
                booking_id = int(data.get("booking_id"))
                
                self.trainer_service.cancel_booking(booking_id)
                logger.info(f"TRAINER_BOOKING_CANCEL: Cancelled booking {booking_id}")
            except Exception as e:
                logger.error(f"Failed to process TRAINER_BOOKING_CANCEL: {str(e)}")
                
            cleaned_text = re.sub(cancel_pattern, "", cleaned_text, flags=re.DOTALL).strip()

        return cleaned_text
