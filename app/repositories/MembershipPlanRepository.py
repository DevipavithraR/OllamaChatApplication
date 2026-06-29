from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.MembershipPlan import MembershipPlan
from app.repositories.BaseRepository import BaseRepository

class MembershipPlanRepository(BaseRepository[MembershipPlan]):
    def __init__(self, db: Session):
        super().__init__(MembershipPlan, db)

    def get_by_name(self, name: str) -> Optional[MembershipPlan]:
        return self.db.query(self.model).filter(self.model.plan_name == name).first()

    def search_plans(self, query: str) -> List[MembershipPlan]:
        return self.db.query(self.model).filter(
            self.model.plan_name.ilike(f"%{query}%") |
            self.model.description.ilike(f"%{query}%") |
            self.model.benefits.ilike(f"%{query}%")
        ).all()
