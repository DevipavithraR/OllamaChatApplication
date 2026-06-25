from typing import List
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.customer import CustomerCreate, CustomerUpdate, CustomerResponse
from app.services.customer import CustomerService

router = APIRouter(prefix="/customers", tags=["Customers"])

@router.post("/", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
def create_customer(customer_in: CustomerCreate, db: Session = Depends(get_db)):
    """
    Register a new customer.
    """
    service = CustomerService(db)
    return service.create_customer(customer_in)

@router.get("/", response_model=List[CustomerResponse])
def get_customers(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Retrieve all customers (paginated).
    """
    service = CustomerService(db)
    return service.get_all_customers(skip, limit)

@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a customer by ID.
    """
    service = CustomerService(db)
    return service.get_customer_by_id(customer_id)

@router.put("/{customer_id}", response_model=CustomerResponse)
def update_customer(customer_id: int, customer_in: CustomerUpdate, db: Session = Depends(get_db)):
    """
    Update a customer's info.
    """
    service = CustomerService(db)
    return service.update_customer(customer_id, customer_in)

@router.delete("/{customer_id}", response_model=CustomerResponse)
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    """
    Remove a customer record.
    """
    service = CustomerService(db)
    return service.delete_customer(customer_id)
