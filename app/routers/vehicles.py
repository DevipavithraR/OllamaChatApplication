from typing import List
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.vehicle_schema import VehicleCreate, VehicleUpdate, VehicleResponse
from app.services.VehicleService import VehicleService

router = APIRouter(prefix="/vehicles", tags=["Vehicles"])

@router.post("/", response_model=VehicleResponse, status_code=status.HTTP_201_CREATED)
def create_vehicle(vehicle_in: VehicleCreate, db: Session = Depends(get_db)):
    """
    Register a new vehicle.
    """
    service = VehicleService(db)
    return service.create_vehicle(vehicle_in)

@router.get("/", response_model=List[VehicleResponse])
def get_vehicles(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Retrieve all vehicles (paginated).
    """
    service = VehicleService(db)
    return service.get_all_vehicles(skip, limit)

@router.get("/{vehicle_id}", response_model=VehicleResponse)
def get_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a vehicle by ID.
    """
    service = VehicleService(db)
    return service.get_vehicle_by_id(vehicle_id)

@router.get("/customer/{customer_id}", response_model=List[VehicleResponse])
def get_vehicles_by_customer(customer_id: int, db: Session = Depends(get_db)):
    """
    Retrieve all vehicles for a customer.
    """
    service = VehicleService(db)
    return service.get_vehicles_by_customer(customer_id)

@router.put("/{vehicle_id}", response_model=VehicleResponse)
def update_vehicle(vehicle_id: int, vehicle_in: VehicleUpdate, db: Session = Depends(get_db)):
    """
    Update a vehicle's info.
    """
    service = VehicleService(db)
    return service.update_vehicle(vehicle_id, vehicle_in)

@router.delete("/{vehicle_id}", response_model=VehicleResponse)
def delete_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    """
    Remove a vehicle record.
    """
    service = VehicleService(db)
    return service.delete_vehicle(vehicle_id)
