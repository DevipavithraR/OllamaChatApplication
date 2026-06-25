from sqlalchemy import Column, Integer, String, Text, Numeric, Boolean
from app.database import Base

class MenuItem(Base):
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)
    price = Column(Numeric(10, 2), nullable=False)
    category = Column(String(50), nullable=False, index=True)  # e.g., appetizers, entrees, desserts, drinks
    is_available = Column(Boolean, default=True, nullable=False)
