from typing import Optional
from sqlalchemy.orm import Session
from app.models.customer import Customer
from app.repositories.BaseRepository import BaseRepository

class CustomerRepository(BaseRepository[Customer]):
    def __init__(self, db: Session):
        super().__init__(Customer, db)

    def get_by_phone_number(self, phone_number: str) -> Optional[Customer]:
        return self.db.query(Customer).filter(Customer.phone_number == phone_number).first()
