from typing import List
from sqlalchemy.orm import Session
from app.models.menu import MenuItem
from app.repositories.menu import MenuRepository
from app.schemas.menu import MenuItemCreate, MenuItemUpdate
from fastapi import HTTPException, status

class MenuService:
    def __init__(self, db: Session):
        self.repository = MenuRepository(db)

    def create_menu_item(self, menu_in: MenuItemCreate) -> MenuItem:
        """
        Create a new menu item. Raises HTTP 400 if item already exists by name.
        """
        existing = self.repository.get_by_name(menu_in.name)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Menu item with name '{menu_in.name}' already exists."
            )

        menu_item = MenuItem(
            name=menu_in.name,
            description=menu_in.description,
            price=menu_in.price,
            category=menu_in.category,
            is_available=menu_in.is_available
        )
        return self.repository.create(menu_item)

    def get_menu_item_by_id(self, menu_item_id: int) -> MenuItem:
        """
        Retrieve a menu item by ID.
        """
        menu_item = self.repository.get(menu_item_id)
        if not menu_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Menu item with ID {menu_item_id} not found."
            )
        return menu_item

    def get_all_menu_items(self, skip: int = 0, limit: int = 100) -> List[MenuItem]:
        """
        Retrieve a paginated list of all menu items.
        """
        return self.repository.get_all(skip, limit)

    def get_available_menu_items(self) -> List[MenuItem]:
        """
        Retrieve all available menu items.
        """
        return self.repository.get_available_items()

    def search_menu_items(self, query: str) -> List[MenuItem]:
        """
        Search for menu items based on query keywords.
        """
        keywords = [word.strip().lower() for word in query.split() if len(word.strip()) > 2]
        # Include original query if it's not empty
        if query.strip() and query.strip().lower() not in keywords:
            keywords.append(query.strip().lower())
        
        return self.repository.search_by_keywords(keywords)

    def update_menu_item(self, menu_item_id: int, menu_in: MenuItemUpdate) -> MenuItem:
        """
        Update an existing menu item.
        """
        menu_item = self.get_menu_item_by_id(menu_item_id)
        update_data = menu_in.model_dump(exclude_unset=True)
        
        if "name" in update_data and update_data["name"] != menu_item.name:
            existing = self.repository.get_by_name(update_data["name"])
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Menu item with name '{update_data['name']}' already exists."
                )

        return self.repository.update(menu_item, update_data)

    def delete_menu_item(self, menu_item_id: int) -> MenuItem:
        """
        Delete a menu item.
        """
        self.get_menu_item_by_id(menu_item_id)
        return self.repository.delete(menu_item_id)
