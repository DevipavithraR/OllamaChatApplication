from typing import List
from sqlalchemy.orm import Session
from app.models.ServiceCatalog import ServiceCatalog
from app.models.Mechanic import Mechanic
from app.repositories.ServiceRepository import ServiceRepository
from app.repositories.MechanicRepository import MechanicRepository

class ServiceSearchService:
    def __init__(self, db: Session):
        self.service_repo = ServiceRepository(db)
        self.mechanic_repo = MechanicRepository(db)

    def search_services(self, query: str) -> List[ServiceCatalog]:
        """
        Search service catalog items matching query keywords.
        """
        keywords = [word.strip().lower() for word in query.split() if len(word.strip()) > 2]
        if query.strip() and query.strip().lower() not in keywords:
            keywords.append(query.strip().lower())
        
        return self.service_repo.search_by_keywords(keywords)

    def search_mechanics(self, query: str) -> List[Mechanic]:
        """
        Search mechanics matching query keywords.
        """
        keywords = [word.strip().lower() for word in query.split() if len(word.strip()) > 2]
        if query.strip() and query.strip().lower() not in keywords:
            keywords.append(query.strip().lower())

        return self.mechanic_repo.search_mechanics(keywords)

    def get_all_services(self) -> List[ServiceCatalog]:
        return self.service_repo.get_all(limit=100)

    def get_all_mechanics(self) -> List[Mechanic]:
        return self.mechanic_repo.get_all(limit=100)
