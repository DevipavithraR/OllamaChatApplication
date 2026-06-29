from sqlalchemy.orm import Session
from typing import List, Optional
from app.repositories.MembershipPlanRepository import MembershipPlanRepository
from app.models.MembershipPlan import MembershipPlan
from app.schemas.membership_plan_schema import MembershipPlanCreate

class MembershipService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = MembershipPlanRepository(db)

    def get_plan_by_id(self, plan_id: int) -> Optional[MembershipPlan]:
        return self.repository.get(plan_id)

    def get_plan_by_name(self, name: str) -> Optional[MembershipPlan]:
        return self.repository.get_by_name(name)

    def get_all_plans(self, skip: int = 0, limit: int = 100) -> List[MembershipPlan]:
        return self.repository.get_all(skip, limit)

    def search_plans(self, query: str) -> List[MembershipPlan]:
        return self.repository.search_plans(query)

    def create_plan(self, obj_in: MembershipPlanCreate) -> MembershipPlan:
        db_obj = MembershipPlan(
            plan_name=obj_in.plan_name,
            duration=obj_in.duration,
            price=obj_in.price,
            benefits=obj_in.benefits,
            description=obj_in.description
        )
        return self.repository.create(db_obj)
