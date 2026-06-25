from typing import List, Optional
from sqlalchemy import or_
from sqlalchemy.orm import Session
from app.models.menu import MenuItem
from app.repositories.base import BaseRepository

class MenuRepository(BaseRepository[MenuItem]):
    def __init__(self, db: Session):
        super().__init__(MenuItem, db)

    def get_by_name(self, name: str) -> Optional[MenuItem]:
        """
        Look up a menu item by its exact name (case-insensitive).
        """
        return self.db.query(MenuItem).filter(MenuItem.name.ilike(name)).first()

    def get_available_items(self) -> List[MenuItem]:
        """
        Get all items that are currently marked as available.
        """
        return self.db.query(MenuItem).filter(MenuItem.is_available == True).all()

    def search_by_keywords(self, keywords: List[str]) -> List[MenuItem]:
        """
        Search for menu items matching any of the provided keywords in name or description.
        Only returns available items.
        """
        if not keywords:
            return []

        filters = []
        for kw in keywords:
            if kw.strip():
                pattern = f"%{kw.strip()}%"
                filters.append(MenuItem.name.ilike(pattern))
                filters.append(MenuItem.description.ilike(pattern))

        if not filters:
            return []

        return (
            self.db.query(MenuItem)
            .filter(MenuItem.is_available == True)
            .filter(or_(*filters))
            .limit(10)
            .all()
        )
