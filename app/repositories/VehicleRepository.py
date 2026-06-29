from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.Vehicle import Vehicle
from app.repositories.BaseRepository import BaseRepository

class VehicleRepository(BaseRepository[Vehicle]):
    def __init__(self, db: Session):
        super().__init__(Vehicle, db)

    def get_by_number(self, vehicle_number: str) -> Optional[Vehicle]:
        """
        Find a vehicle by its vehicle number.
        """
        return self.db.query(Vehicle).filter(Vehicle.vehicle_number == vehicle_number).first()

    def get_by_customer_id(self, customer_id: int) -> List[Vehicle]:
        """
        Retrieve all vehicles owned by a customer.
        """
        return self.db.query(Vehicle).filter(Vehicle.customer_id == customer_id).all()
