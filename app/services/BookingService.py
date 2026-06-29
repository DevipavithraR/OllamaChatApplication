from datetime import datetime, timedelta
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.ServiceBooking import ServiceBooking
from app.models.Customer import Customer
from app.models.Vehicle import Vehicle
from app.models.ServiceCatalog import ServiceCatalog
from app.models.Mechanic import Mechanic
from app.repositories.ServiceBookingRepository import ServiceBookingRepository
from app.repositories.CustomerRepository import CustomerRepository
from app.repositories.VehicleRepository import VehicleRepository
from app.repositories.ServiceRepository import ServiceRepository
from app.repositories.MechanicRepository import MechanicRepository
from app.schemas.service_booking_schema import ServiceBookingCreate, ServiceBookingCreateWithCustomer, ServiceBookingUpdate
from app.schemas.customer_schema import CustomerCreate
from app.schemas.vehicle_schema import VehicleCreate
from fastapi import HTTPException, status
import logging

logger = logging.getLogger("app.services.BookingService")

def parse_duration_to_hours(duration_str: str) -> float:
    try:
        parts = duration_str.lower().split()
        if len(parts) >= 2:
            val = float(parts[0])
            unit = parts[1]
            if "hour" in unit:
                return val
            elif "minute" in unit:
                return val / 60.0
    except Exception as e:
        logger.warning(f"Failed to parse duration string '{duration_str}': {str(e)}")
    return 2.0 # default fallback

class BookingService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = ServiceBookingRepository(db)
        self.customer_repo = CustomerRepository(db)
        self.vehicle_repo = VehicleRepository(db)
        self.service_repo = ServiceRepository(db)
        self.mechanic_repo = MechanicRepository(db)

    def create_booking(self, booking_in: ServiceBookingCreate) -> ServiceBooking:
        """
        Create a booking for an existing customer, vehicle, and service.
        Allocates an available mechanic.
        """
        # Verify customer, vehicle, and service exist
        customer = self.customer_repo.get(booking_in.customer_id)
        if not customer:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Customer ID {booking_in.customer_id} not found.")

        vehicle = self.vehicle_repo.get(booking_in.vehicle_id)
        if not vehicle:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vehicle ID {booking_in.vehicle_id} not found.")

        service = self.service_repo.get(booking_in.service_id)
        if not service:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Service ID {booking_in.service_id} not found.")

        # Find and assign an available mechanic
        mechanic_id = booking_in.mechanic_id
        if not mechanic_id:
            mechanic = self._find_available_mechanic(service)
            if mechanic:
                mechanic_id = mechanic.mechanic_id
                logger.info(f"Assigned mechanic {mechanic.name} to new booking.")

        # Calculate estimated completion
        hours = parse_duration_to_hours(service.estimated_duration)
        est_completion = booking_in.service_date + timedelta(hours=hours)

        booking = ServiceBooking(
            customer_id=booking_in.customer_id,
            vehicle_id=booking_in.vehicle_id,
            mechanic_id=mechanic_id,
            service_id=booking_in.service_id,
            service_date=booking_in.service_date,
            booking_status=booking_in.booking_status,
            estimated_completion=est_completion,
            customer_notes=booking_in.customer_notes
        )
        return self.repository.create(booking)

    def create_booking_with_customer(self, booking_in: ServiceBookingCreateWithCustomer) -> ServiceBooking:
        """
        Create a service booking by registering/retrieving customer and vehicle automatically.
        """
        # 1. Retrieve or Create Customer
        customer = self.customer_repo.get_by_phone(booking_in.customer_phone)
        if not customer:
            logger.info(f"Customer not found for phone {booking_in.customer_phone}. Creating customer...")
            customer = Customer(
                name=booking_in.customer_name,
                phone_number=booking_in.customer_phone,
                email=booking_in.customer_email
            )
            customer = self.customer_repo.create(customer)

        # 2. Retrieve or Create Vehicle
        vehicle = self.vehicle_repo.get_by_number(booking_in.vehicle_number)
        if not vehicle:
            logger.info(f"Vehicle not found for number {booking_in.vehicle_number}. Creating vehicle...")
            vehicle = Vehicle(
                customer_id=customer.customer_id,
                vehicle_number=booking_in.vehicle_number,
                vehicle_brand=booking_in.vehicle_brand or "Unknown",
                vehicle_model=booking_in.vehicle_model or "Unknown",
                fuel_type="Petrol", # default
                manufacturing_year=datetime.now().year # default
            )
            vehicle = self.vehicle_repo.create(vehicle)

        # 3. Look up Service
        service = self.service_repo.get_by_name(booking_in.service_name)
        if not service:
            # Fallback check - search by keywords or throw
            searched = self.service_repo.search_by_keywords([booking_in.service_name])
            if searched:
                service = searched[0]
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Service '{booking_in.service_name}' not found in the service center catalog."
                )

        # 4. Find and assign an available mechanic
        mechanic = self._find_available_mechanic(service)
        mechanic_id = mechanic.mechanic_id if mechanic else None

        # Calculate completion
        hours = parse_duration_to_hours(service.estimated_duration)
        est_completion = booking_in.service_date + timedelta(hours=hours)

        booking = ServiceBooking(
            customer_id=customer.customer_id,
            vehicle_id=vehicle.vehicle_id,
            mechanic_id=mechanic_id,
            service_id=service.service_id,
            service_date=booking_in.service_date,
            booking_status="Scheduled",
            estimated_completion=est_completion,
            customer_notes=booking_in.customer_notes
        )
        return self.repository.create(booking)

    def _find_available_mechanic(self, service: ServiceCatalog) -> Optional[Mechanic]:
        """
        Finds an available mechanic specializing in the service, or any available mechanic as fallback.
        """
        available = self.mechanic_repo.get_available_mechanics()
        if not available:
            return None

        # Attempt to match specialization
        for mech in available:
            if mech.specialization.lower() in service.service_name.lower() or service.service_name.lower() in mech.specialization.lower():
                return mech

        # Second attempt matching by keywords
        service_keywords = [w.lower() for w in service.service_name.split() if len(w) > 3]
        for mech in available:
            if any(kw in mech.specialization.lower() for kw in service_keywords):
                return mech

        # Fallback to first available mechanic
        return available[0]

    def get_booking_by_id(self, booking_id: int) -> ServiceBooking:
        booking = self.repository.get(booking_id)
        if not booking:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Service Booking with ID {booking_id} not found."
            )
        return booking

    def get_bookings_by_customer_phone(self, phone_number: str) -> List[ServiceBooking]:
        return self.repository.get_by_customer_phone(phone_number)

    def get_all_bookings(self, skip: int = 0, limit: int = 100) -> List[ServiceBooking]:
        return self.repository.get_all(skip, limit)

    def update_booking(self, booking_id: int, booking_in: ServiceBookingUpdate) -> ServiceBooking:
        booking = self.get_booking_by_id(booking_id)
        update_data = booking_in.model_dump(exclude_unset=True)

        # Re-calculate estimated completion if service_date or estimated_completion changes
        if "service_date" in update_data and "estimated_completion" not in update_data:
            service = self.service_repo.get(booking.service_id)
            if service:
                hours = parse_duration_to_hours(service.estimated_duration)
                update_data["estimated_completion"] = update_data["service_date"] + timedelta(hours=hours)

        return self.repository.update(booking, update_data)

    def cancel_booking(self, booking_id: int) -> ServiceBooking:
        booking = self.get_booking_by_id(booking_id)
        booking.booking_status = "Cancelled"
        self.db.commit()
        self.db.refresh(booking)
        return booking

    def delete_booking(self, booking_id: int) -> ServiceBooking:
        self.get_booking_by_id(booking_id)
        return self.repository.delete(booking_id)
