from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.Vehicle import Vehicle
from app.repositories.VehicleRepository import VehicleRepository
from app.schemas.vehicle_schema import VehicleCreate, VehicleUpdate
from fastapi import HTTPException, status

class VehicleService:
    def __init__(self, db: Session):
        self.repository = VehicleRepository(db)

    def create_vehicle(self, vehicle_in: VehicleCreate) -> Vehicle:
        """
        Create a new vehicle. Raises HTTP 400 if vehicle number already registered.
        """
        existing = self.repository.get_by_number(vehicle_in.vehicle_number)
        if existing:
            # If it already exists for the same customer, just return it. Else error.
            if existing.customer_id == vehicle_in.customer_id:
                return existing
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Vehicle with number {vehicle_in.vehicle_number} is already registered under another customer."
            )

        vehicle = Vehicle(
            customer_id=vehicle_in.customer_id,
            vehicle_number=vehicle_in.vehicle_number,
            vehicle_brand=vehicle_in.vehicle_brand,
            vehicle_model=vehicle_in.vehicle_model,
            fuel_type=vehicle_in.fuel_type,
            manufacturing_year=vehicle_in.manufacturing_year
        )
        return self.repository.create(vehicle)

    def get_vehicle_by_id(self, vehicle_id: int) -> Vehicle:
        """
        Get vehicle by ID. Raises 404 if not found.
        """
        vehicle = self.repository.get(vehicle_id)
        if not vehicle:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Vehicle with ID {vehicle_id} not found."
            )
        return vehicle

    def get_vehicle_by_number(self, vehicle_number: str) -> Optional[Vehicle]:
        """
        Find vehicle by vehicle number.
        """
        return self.repository.get_by_number(vehicle_number)

    def get_vehicles_by_customer(self, customer_id: int) -> List[Vehicle]:
        """
        Retrieve all vehicles belonging to a customer.
        """
        return self.repository.get_by_customer_id(customer_id)

    def get_all_vehicles(self, skip: int = 0, limit: int = 100) -> List[Vehicle]:
        """
        Get all vehicles.
        """
        return self.repository.get_all(skip, limit)

    def update_vehicle(self, vehicle_id: int, vehicle_in: VehicleUpdate) -> Vehicle:
        """
        Update vehicle information.
        """
        vehicle = self.get_vehicle_by_id(vehicle_id)
        update_data = vehicle_in.model_dump(exclude_unset=True)

        if "vehicle_number" in update_data and update_data["vehicle_number"] != vehicle.vehicle_number:
            existing = self.repository.get_by_number(update_data["vehicle_number"])
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Vehicle with number {update_data['vehicle_number']} already exists."
                )

        return self.repository.update(vehicle, update_data)

    def delete_vehicle(self, vehicle_id: int) -> Vehicle:
        """
        Delete a vehicle.
        """
        self.get_vehicle_by_id(vehicle_id)
        return self.repository.delete(vehicle_id)
