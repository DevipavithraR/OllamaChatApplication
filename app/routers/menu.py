from typing import List
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.menu import MenuItemCreate, MenuItemUpdate, MenuItemResponse
from app.services.menu import MenuService

router = APIRouter(prefix="/menu", tags=["Menu"])

@router.post("/", response_model=MenuItemResponse, status_code=status.HTTP_201_CREATED)
def create_menu_item(menu_in: MenuItemCreate, db: Session = Depends(get_db)):
    """
    Add a new item to the restaurant menu.
    """
    service = MenuService(db)
    return service.create_menu_item(menu_in)

@router.get("/", response_model=List[MenuItemResponse])
def get_menu_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Retrieve all menu items (paginated).
    """
    service = MenuService(db)
    return service.get_all_menu_items(skip, limit)

@router.get("/search", response_model=List[MenuItemResponse])
def search_menu_items(q: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    """
    Search menu items using keyword matching on name or description.
    """
    service = MenuService(db)
    return service.search_menu_items(q)

@router.get("/{menu_item_id}", response_model=MenuItemResponse)
def get_menu_item(menu_item_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a menu item by ID.
    """
    service = MenuService(db)
    return service.get_menu_item_by_id(menu_item_id)

@router.put("/{menu_item_id}", response_model=MenuItemResponse)
def update_menu_item(
    menu_item_id: int,
    menu_in: MenuItemUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a menu item's details.
    """
    service = MenuService(db)
    return service.update_menu_item(menu_item_id, menu_in)

@router.delete("/{menu_item_id}", response_model=MenuItemResponse)
def delete_menu_item(menu_item_id: int, db: Session = Depends(get_db)):
    """
    Remove a menu item from the system.
    """
    service = MenuService(db)
    return service.delete_menu_item(menu_item_id)
