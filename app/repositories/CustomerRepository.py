from typing import Optional
from sqlalchemy.orm import Session
from app.models.Customer import Customer
from app.repositories.BaseRepository import BaseRepository

class CustomerRepository(BaseRepository[Customer]):
    def __init__(self, db: Session):
        super().__init__(Customer, db)

    def get_by_phone(self, phone_number: str) -> Optional[Customer]:
        """
        Find a customer by phone number.
        """
        return self.db.query(Customer).filter(Customer.phone_number == phone_number).first()

    def get_by_email(self, email: str) -> Optional[Customer]:
        """
        Find a customer by email address.
        """
        return self.db.query(Customer).filter(Customer.email == email).first()
