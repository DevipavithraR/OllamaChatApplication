from typing import List
from fastapi import APIRouter, Depends, Query, status, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.service_schema import ServiceCatalogCreate, ServiceCatalogUpdate, ServiceCatalogResponse
from app.repositories.ServiceRepository import ServiceRepository

router = APIRouter(prefix="/services", tags=["Services"])

@router.post("/", response_model=ServiceCatalogResponse, status_code=status.HTTP_201_CREATED)
def create_service(service_in: ServiceCatalogCreate, db: Session = Depends(get_db)):
    """
    Add a new service package to the catalog.
    """
    repo = ServiceRepository(db)
    existing = repo.get_by_name(service_in.service_name)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Service with name '{service_in.service_name}' already exists."
        )
    
    from app.models.ServiceCatalog import ServiceCatalog
    service = ServiceCatalog(
        service_name=service_in.service_name,
        description=service_in.description,
        estimated_duration=service_in.estimated_duration,
        service_cost=service_in.service_cost
    )
    return repo.create(service)

@router.get("/", response_model=List[ServiceCatalogResponse])
def get_services(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Retrieve all services (paginated).
    """
    repo = ServiceRepository(db)
    return repo.get_all(skip, limit)

@router.get("/{service_id}", response_model=ServiceCatalogResponse)
def get_service(service_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a service from the catalog by ID.
    """
    repo = ServiceRepository(db)
    service = repo.get(service_id)
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Service with ID {service_id} not found."
        )
    return service

@router.put("/{service_id}", response_model=ServiceCatalogResponse)
def update_service(service_id: int, service_in: ServiceCatalogUpdate, db: Session = Depends(get_db)):
    """
    Update a service package in the catalog.
    """
    repo = ServiceRepository(db)
    service = repo.get(service_id)
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Service with ID {service_id} not found."
        )
    update_data = service_in.model_dump(exclude_unset=True)
    
    if "service_name" in update_data and update_data["service_name"] != service.service_name:
        existing = repo.get_by_name(update_data["service_name"])
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Service with name '{update_data['service_name']}' already exists."
            )

    return repo.update(service, update_data)

@router.delete("/{service_id}", response_model=ServiceCatalogResponse)
def delete_service(service_id: int, db: Session = Depends(get_db)):
    """
    Remove a service package from the catalog.
    """
    repo = ServiceRepository(db)
    service = repo.get(service_id)
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Service with ID {service_id} not found."
        )
    return repo.delete(service_id)
