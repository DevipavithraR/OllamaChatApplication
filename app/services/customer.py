from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.customer import Customer
from app.repositories.customer import CustomerRepository
from app.schemas.customer import CustomerCreate, CustomerUpdate
from fastapi import HTTPException, status

class CustomerService:
    def __init__(self, db: Session):
        self.repository = CustomerRepository(db)

    def create_customer(self, customer_in: CustomerCreate) -> Customer:
        """
        Create a new customer. Raises HTTP 400 if the phone number already exists.
        """
        existing = self.repository.get_by_phone(customer_in.phone)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Customer with phone number {customer_in.phone} already exists."
            )
        
        customer = Customer(
            name=customer_in.name,
            phone=customer_in.phone,
            email=customer_in.email
        )
        return self.repository.create(customer)

    def get_customer_by_id(self, customer_id: int) -> Customer:
        """
        Get customer by ID. Raises HTTP 404 if not found.
        """
        customer = self.repository.get(customer_id)
        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Customer with ID {customer_id} not found."
            )
        return customer

    def get_customer_by_phone(self, phone: str) -> Optional[Customer]:
        """
        Retrieve customer by phone.
        """
        return self.repository.get_by_phone(phone)

    def get_all_customers(self, skip: int = 0, limit: int = 100) -> List[Customer]:
        """
        Retrieve a paginated list of customers.
        """
        return self.repository.get_all(skip, limit)

    def update_customer(self, customer_id: int, customer_in: CustomerUpdate) -> Customer:
        """
        Update an existing customer.
        """
        customer = self.get_customer_by_id(customer_id)
        update_data = customer_in.model_dump(exclude_unset=True)
        
        # If phone is changing, verify uniqueness
        if "phone" in update_data and update_data["phone"] != customer.phone:
            existing = self.repository.get_by_phone(update_data["phone"])
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Customer with phone number {update_data['phone']} already exists."
                )

        return self.repository.update(customer, update_data)

    def delete_customer(self, customer_id: int) -> Customer:
        """
        Delete a customer by ID.
        """
        customer = self.get_customer_by_id(customer_id)
        return self.repository.delete(customer_id)
