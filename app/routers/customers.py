from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.customer_schema import CustomerCreate, CustomerUpdate, CustomerResponse
from app.services.CustomerService import CustomerService

router = APIRouter(prefix="/customers", tags=["Customers"])

@router.post("", response_model=CustomerResponse)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    service = CustomerService(db)
    return service.create_customer(customer)

@router.get("", response_model=List[CustomerResponse])
def get_all_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    service = CustomerService(db)
    return service.get_all_customers(skip, limit)

@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    service = CustomerService(db)
    return service.get_customer_by_id(customer_id)

@router.put("/{customer_id}", response_model=CustomerResponse)
def update_customer(customer_id: int, customer: CustomerUpdate, db: Session = Depends(get_db)):
    service = CustomerService(db)
    return service.update_customer(customer_id, customer)

@router.delete("/{customer_id}", response_model=CustomerResponse)
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    service = CustomerService(db)
    return service.delete_customer(customer_id)
