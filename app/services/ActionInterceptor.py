import re
import json
import logging
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session
from app.services.CustomerService import CustomerService
from app.services.VehicleService import VehicleService
from app.services.BookingService import BookingService
from app.repositories.ConversationRepository import ConversationRepository
from app.schemas.customer_schema import CustomerCreate
from app.schemas.vehicle_schema import VehicleCreate
from app.schemas.service_booking_schema import ServiceBookingCreateWithCustomer

logger = logging.getLogger("app.services.ActionInterceptor")

class ActionInterceptor:
    def __init__(self, db: Session):
        self.db = db
        self.customer_service = CustomerService(db)
        self.vehicle_service = VehicleService(db)
        self.booking_service = BookingService(db)
        self.conversation_repo = ConversationRepository(db)

    def intercept_and_execute(self, conversation_id: int, response_text: str) -> tuple[str, Optional[int]]:
        """
        Intercepts and processes CUSTOMER_IDENTIFY, VEHICLE_REGISTER, SERVICE_BOOKING_CONFIRM,
        SERVICE_STATUS, and SERVICE_CANCEL tags. Returns the cleaned response text and linked customer_id.
        """
        cleaned_text = response_text
        customer_id = None

        # 1. CUSTOMER_IDENTIFY Interception
        ident_pattern = r"```CUSTOMER_IDENTIFY:?\s*(\{.*?\})\s*```"
        ident_match = re.search(ident_pattern, response_text, re.DOTALL)
        if ident_match:
            try:
                data = json.loads(ident_match.group(1))
                name = data.get("name")
                phone = data.get("phone")
                logger.info(f"Intercepted CUSTOMER_IDENTIFY: name={name}, phone={phone}")
                if phone:
                    customer = self.customer_service.get_customer_by_phone(phone)
                    if not customer and name:
                        customer = self.customer_service.create_customer(
                            CustomerCreate(name=name, phone_number=phone)
                        )
                    if customer:
                        customer_id = customer.customer_id
                        self.conversation_repo.link_customer(conversation_id, customer_id)
                        logger.info(f"Linked conversation {conversation_id} to customer {customer_id}")
            except Exception as e:
                logger.error(f"Error handling CUSTOMER_IDENTIFY: {str(e)}")
            cleaned_text = re.sub(ident_pattern, "", cleaned_text, flags=re.DOTALL).strip()

        # 2. VEHICLE_REGISTER Interception
        vehicle_pattern = r"```VEHICLE_REGISTER:?\s*(\{.*?\})\s*```"
        vehicle_match = re.search(vehicle_pattern, response_text, re.DOTALL)
        if vehicle_match:
            try:
                data = json.loads(vehicle_match.group(1))
                cust_name = data.get("customer_name")
                phone = data.get("phone")
                vehicle_num = data.get("vehicle_number")
                brand = data.get("vehicle_brand", "Unknown")
                model = data.get("vehicle_model", "Unknown")
                fuel = data.get("fuel_type", "Petrol")
                year = int(data.get("manufacturing_year", datetime.now().year))

                logger.info(f"Intercepted VEHICLE_REGISTER: phone={phone}, vehicle_num={vehicle_num}")
                
                # Check / Create customer
                customer = self.customer_service.get_customer_by_phone(phone)
                if not customer and cust_name:
                    customer = self.customer_service.create_customer(
                        CustomerCreate(name=cust_name, phone_number=phone)
                    )
                
                if customer:
                    customer_id = customer.customer_id
                    self.conversation_repo.link_customer(conversation_id, customer_id)
                    
                    # Create vehicle
                    self.vehicle_service.create_vehicle(
                        VehicleCreate(
                            customer_id=customer_id,
                            vehicle_number=vehicle_num,
                            vehicle_brand=brand,
                            vehicle_model=model,
                            fuel_type=fuel,
                            manufacturing_year=year
                        )
                    )
                    logger.info(f"Registered vehicle {vehicle_num} for customer {customer_id}")
            except Exception as e:
                logger.error(f"Error handling VEHICLE_REGISTER: {str(e)}")
            cleaned_text = re.sub(vehicle_pattern, "", cleaned_text, flags=re.DOTALL).strip()

        # 3. SERVICE_BOOKING_CONFIRM Interception
        booking_pattern = r"```SERVICE_BOOKING_CONFIRM:?\s*(\{.*?\})\s*```"
        booking_match = re.search(booking_pattern, response_text, re.DOTALL)
        if booking_match:
            try:
                data = json.loads(booking_match.group(1))
                cust_name = data.get("customer_name")
                phone = data.get("phone")
                vehicle_num = data.get("vehicle_number")
                service_name = data.get("service_name")
                service_date_str = data.get("service_date")
                notes = data.get("customer_notes")

                logger.info(f"Intercepted SERVICE_BOOKING_CONFIRM: phone={phone}, service={service_name}, date={service_date_str}")
                
                # Parse datetime
                service_date = datetime.strptime(service_date_str, "%Y-%m-%d %H:%M:%S")

                dto = ServiceBookingCreateWithCustomer(
                    customer_name=cust_name,
                    customer_phone=phone,
                    vehicle_number=vehicle_num,
                    service_name=service_name,
                    service_date=service_date,
                    customer_notes=notes
                )
                booking = self.booking_service.create_booking_with_customer(dto)
                customer_id = booking.customer_id
                self.conversation_repo.link_customer(conversation_id, customer_id)
                logger.info(f"Successfully booked service ID {booking.booking_id} for customer {customer_id}")
            except Exception as e:
                logger.error(f"Error handling SERVICE_BOOKING_CONFIRM: {str(e)}")
            cleaned_text = re.sub(booking_pattern, "", cleaned_text, flags=re.DOTALL).strip()

        # 4. SERVICE_STATUS Interception
        status_pattern = r"```SERVICE_STATUS:?\s*(\{.*?\})\s*```"
        status_match = re.search(status_pattern, response_text, re.DOTALL)
        if status_match:
            try:
                data = json.loads(status_match.group(1))
                booking_id = int(data.get("booking_id"))
                logger.info(f"Intercepted SERVICE_STATUS check for booking {booking_id}")
                booking = self.booking_service.get_booking_by_id(booking_id)
                if booking:
                    customer_id = booking.customer_id
                    self.conversation_repo.link_customer(conversation_id, customer_id)
            except Exception as e:
                logger.error(f"Error handling SERVICE_STATUS check: {str(e)}")
            cleaned_text = re.sub(status_pattern, "", cleaned_text, flags=re.DOTALL).strip()

        # 5. SERVICE_CANCEL Interception
        cancel_pattern = r"```SERVICE_CANCEL:?\s*(\{.*?\})\s*```"
        cancel_match = re.search(cancel_pattern, response_text, re.DOTALL)
        if cancel_match:
            try:
                data = json.loads(cancel_match.group(1))
                booking_id = int(data.get("booking_id"))
                logger.info(f"Intercepted SERVICE_CANCEL for booking {booking_id}")
                booking = self.booking_service.cancel_booking(booking_id)
                if booking:
                    customer_id = booking.customer_id
                    self.conversation_repo.link_customer(conversation_id, customer_id)
            except Exception as e:
                logger.error(f"Error handling SERVICE_CANCEL: {str(e)}")
            cleaned_text = re.sub(cancel_pattern, "", cleaned_text, flags=re.DOTALL).strip()

        # If customer_id was not updated, try loading from conversation
        if not customer_id:
            conv = self.conversation_repo.get(conversation_id)
            if conv:
                customer_id = conv.customer_id

        return cleaned_text, customer_id
