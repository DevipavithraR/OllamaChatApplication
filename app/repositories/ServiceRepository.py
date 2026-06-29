from typing import List, Optional
from sqlalchemy import or_
from sqlalchemy.orm import Session
from app.models.ServiceCatalog import ServiceCatalog
from app.repositories.BaseRepository import BaseRepository

class ServiceRepository(BaseRepository[ServiceCatalog]):
    def __init__(self, db: Session):
        super().__init__(ServiceCatalog, db)

    def get_by_name(self, service_name: str) -> Optional[ServiceCatalog]:
        """
        Find a service by its exact name (case-insensitive).
        """
        return self.db.query(ServiceCatalog).filter(ServiceCatalog.service_name.ilike(service_name)).first()

    def search_by_keywords(self, keywords: List[str]) -> List[ServiceCatalog]:
        """
        Search service catalog items matching keywords in name or description.
        """
        if not keywords:
            return []

        filters = []
        for kw in keywords:
            if kw.strip():
                pattern = f"%{kw.strip()}%"
                filters.append(ServiceCatalog.service_name.ilike(pattern))
                filters.append(ServiceCatalog.description.ilike(pattern))

        if not filters:
            return []

        return (
            self.db.query(ServiceCatalog)
            .filter(or_(*filters))
            .limit(10)
            .all()
        )
