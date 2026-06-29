from sqlalchemy.orm import Session
from typing import List, Optional
from app.repositories.TrainerRepository import TrainerRepository
from app.repositories.TrainerBookingRepository import TrainerBookingRepository
from app.models.Trainer import Trainer
from app.models.TrainerBooking import TrainerBooking
from app.schemas.trainer_schema import TrainerCreate, TrainerUpdate
from app.schemas.trainer_booking_schema import TrainerBookingCreate, TrainerBookingUpdate

class TrainerSearchService:
    def __init__(self, db: Session):
        self.db = db
        self.trainer_repository = TrainerRepository(db)
        self.booking_repository = TrainerBookingRepository(db)

    def get_trainer_by_id(self, trainer_id: int) -> Optional[Trainer]:
        return self.trainer_repository.get(trainer_id)

    def get_trainer_by_name(self, name: str) -> Optional[Trainer]:
        return self.trainer_repository.get_by_name(name)

    def get_all_trainers(self, skip: int = 0, limit: int = 100) -> List[Trainer]:
        return self.trainer_repository.get_all(skip, limit)

    def search_trainers(self, query: str) -> List[Trainer]:
        return self.trainer_repository.search_trainers(query)

    def create_trainer(self, obj_in: TrainerCreate) -> Trainer:
        db_obj = Trainer(
            trainer_name=obj_in.trainer_name,
            specialization=obj_in.specialization,
            experience=obj_in.experience,
            available_days=obj_in.available_days,
            available_time=obj_in.available_time,
            session_fee=obj_in.session_fee,
            status=obj_in.status
        )
        return self.trainer_repository.create(db_obj)

    def update_trainer(self, trainer_id: int, obj_in: TrainerUpdate) -> Optional[Trainer]:
        db_obj = self.get_trainer_by_id(trainer_id)
        if not db_obj:
            return None
        update_data = obj_in.model_dump(exclude_unset=True)
        return self.trainer_repository.update(db_obj, update_data)

    def delete_trainer(self, trainer_id: int) -> Optional[Trainer]:
        return self.trainer_repository.delete(trainer_id)

    # Booking operations
    def get_all_bookings(self, skip: int = 0, limit: int = 100) -> List[TrainerBooking]:
        return self.booking_repository.get_all(skip, limit)

    def get_booking_by_id(self, booking_id: int) -> Optional[TrainerBooking]:
        return self.booking_repository.get(booking_id)

    def create_booking(self, obj_in: TrainerBookingCreate) -> TrainerBooking:
        db_obj = TrainerBooking(
            member_id=obj_in.member_id,
            trainer_id=obj_in.trainer_id,
            booking_datetime=obj_in.booking_datetime,
            status=obj_in.status,
            training_goal=obj_in.training_goal
        )
        return self.booking_repository.create(db_obj)

    def update_booking(self, booking_id: int, obj_in: TrainerBookingUpdate) -> Optional[TrainerBooking]:
        db_obj = self.get_booking_by_id(booking_id)
        if not db_obj:
            return None
        update_data = obj_in.model_dump(exclude_unset=True)
        return self.booking_repository.update(db_obj, update_data)

    def cancel_booking(self, booking_id: int) -> Optional[TrainerBooking]:
        db_obj = self.get_booking_by_id(booking_id)
        if not db_obj:
            return None
        return self.booking_repository.update(db_obj, {"status": "CANCELLED"})

    def delete_booking(self, booking_id: int) -> Optional[TrainerBooking]:
        return self.booking_repository.delete(booking_id)
