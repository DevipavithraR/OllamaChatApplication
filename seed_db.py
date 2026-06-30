import logging
from app.database import SessionLocal, engine, Base
from app.models.menu import MenuItem

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("seed")

MENU_ITEMS = [
    # Appetizers
    {"name": "Samosa Chaat", "description": "Crispy pastries filled with spiced potatoes and peas, topped with seasoned chickpeas, yogurt, mint, and sweet tamarind chutneys.", "price": 9.00, "category": "appetizers", "is_available": True},
    {"name": "Paneer Tikka", "description": "Cottage cheese cubes marinated in spiced yogurt and grilled to a charred finish in our traditional clay tandoor oven.", "price": 12.50, "category": "appetizers", "is_available": True},
    {"name": "Chicken Tikka", "description": "Tender chicken thigh chunks marinated in yogurt and hand-ground spices, skewered and charred to juicy perfection.", "price": 13.50, "category": "appetizers", "is_available": True},
    {"name": "Veg Pakoras", "description": "Assorted crispy fritters made of spinach, onion, and potato battered in spiced chickpea flour.", "price": 8.00, "category": "appetizers", "is_available": True},
    
    # Entrees
    {"name": "Butter Chicken", "description": "Succulent grilled chicken chunks simmered in a rich, creamy, buttery tomato sauce infused with fenugreek leaves.", "price": 18.99, "category": "entrees", "is_available": True},
    {"name": "Lamb Rogan Josh", "description": "Tender lamb shoulder slow-cooked in a classic Kashmiri gravy flavored with caramelized onions, yogurt, ginger, garlic, and aromatic spices.", "price": 21.00, "category": "entrees", "is_available": True},
    {"name": "Paneer Butter Masala", "description": "Fresh paneer cubes simmered in a silky, creamy tomato and cashew-nut gravy flavored with traditional spices.", "price": 16.50, "category": "entrees", "is_available": True},
    {"name": "Chicken Biryani", "description": "Fragrant long-grain basmati rice layered with spiced chicken, saffron, fresh mint, and caramelized onions, slow-cooked in traditional Dum style.", "price": 17.50, "category": "entrees", "is_available": True},
    {"name": "Dal Makhani", "description": "Creamy, slow-cooked black lentils and red kidney beans simmered overnight on low charcoal heat, finished with fresh cream and butter.", "price": 14.50, "category": "entrees", "is_available": True},
    
    # Desserts
    {"name": "Gulab Jamun", "description": "Golden brown milk-solid dumplings deep-fried and soaked in a warm sugar syrup flavored with green cardamom and rose water.", "price": 6.50, "category": "desserts", "is_available": True},
    {"name": "Mango Kulfi", "description": "Traditional dense and creamy Indian ice cream flavored with sweet Alphonso mango pulp, saffron, and crushed pistachios.", "price": 7.50, "category": "desserts", "is_available": True},
    {"name": "Rasmalai", "description": "Soft and spongy flattened cottage cheese patties soaked in a chilled, sweet cardamom-infused milk, garnished with pistachios and almond flakes.", "price": 8.00, "category": "desserts", "is_available": True},
    
    # Drinks
    {"name": "Mango Lassi", "description": "A refreshing, sweet yogurt-based drink blended with ripe mango pulp and a touch of cardamom.", "price": 4.50, "category": "drinks", "is_available": True},
    {"name": "Masala Chai", "description": "Freshly brewed Indian tea with milk, black tea leaves, crushed ginger, cardamom, cinnamon, and cloves.", "price": 3.50, "category": "drinks", "is_available": True},
    {"name": "Kingfisher Beer", "description": "Crisp, premium Indian lager, exceptionally well-suited to balance aromatic and spicy Indian dishes.", "price": 7.00, "category": "drinks", "is_available": True}
]

def seed_database():
    logger.info("Initializing database tables...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Delete existing menu items to update database
        logger.info("Clearing existing menu items to replace with Indian menu...")
        db.query(MenuItem).delete()
        db.commit()

        logger.info("Seeding new Indian menu items...")
        for item_data in MENU_ITEMS:
            item = MenuItem(**item_data)
            db.add(item)
        db.commit()
        logger.info("Seeding completed successfully!")
    except Exception as e:
        db.rollback()
        logger.error(f"Error seeding database: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
