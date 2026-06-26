import logging
from app.database import SessionLocal, engine, Base
from app.models.menu import MenuItem

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("seed")

MENU_ITEMS = [
    {"name": "Caprese Salad", "description": "Fresh mozzarella, ripe tomatoes, sweet basil leaves, drizzled with balsamic glaze and extra virgin olive oil.", "price": 11.50, "category": "appetizers", "is_available": True},
    {"name": "Bruschetta", "description": "Grilled bread rubbed with garlic, topped with diced tomatoes, fresh basil, and extra virgin olive oil.", "price": 9.00, "category": "appetizers", "is_available": True},
    {"name": "Minestrone Soup", "description": "Classic Italian vegetable soup made with tomatoes, beans, onions, celery, carrots, and pasta.", "price": 8.50, "category": "appetizers", "is_available": True},
    {"name": "Margherita Pizza", "description": "Traditional Italian pizza topped with tomato sauce, fresh mozzarella, and sweet basil.", "price": 14.50, "category": "entrees", "is_available": True},
    {"name": "Fettuccine Alfredo", "description": "Fettuccine pasta tossed in a rich, creamy sauce made of parmesan cheese and butter.", "price": 17.50, "category": "entrees", "is_available": True},
    {"name": "Spaghetti Carbonara", "description": "Spaghetti tossed with crispy pancetta, eggs, pecorino romano cheese, and cracked black pepper.", "price": 18.00, "category": "entrees", "is_available": True},
    {"name": "Grilled Ribeye Steak", "description": "Premium ribeye steak grilled to order, served with garlic mashed potatoes and roasted asparagus.", "price": 32.00, "category": "entrees", "is_available": True},
    {"name": "Chicken Parmigiana", "description": "Breaded chicken breast baked with tomato sauce and mozzarella cheese, served over spaghetti.", "price": 21.00, "category": "entrees", "is_available": True},
    {"name": "Tiramisu", "description": "Classic Italian dessert made of coffee-dipped ladyfingers layered with whipped mascarpone cheese and cocoa.", "price": 8.50, "category": "desserts", "is_available": True},
    {"name": "Panna Cotta", "description": "Creamy Italian pudding sweetened with sugar and vanilla, topped with a fresh raspberry coulis.", "price": 7.50, "category": "desserts", "is_available": True},
    {"name": "Gelato Trio", "description": "Three scoops of authentic Italian gelato. Flavors: dark chocolate, pistachio, and Tahitian vanilla.", "price": 6.50, "category": "desserts", "is_available": True},
    {"name": "Chardonnay", "description": "Crisp white wine with notes of apple, pear, and a touch of oak. Glass/Bottle.", "price": 9.50, "category": "drinks", "is_available": True},
    {"name": "Chianti Classico", "description": "Bold red wine with cherry, leather, and vanilla tasting notes. Glass/Bottle.", "price": 11.00, "category": "drinks", "is_available": True},
    {"name": "San Pellegrino", "description": "Sparkling natural mineral water from the Italian Alps.", "price": 4.50, "category": "drinks", "is_available": True},
    {"name": "Espresso", "description": "Rich and intense shot of freshly brewed espresso.", "price": 3.50, "category": "drinks", "is_available": True}
]

def seed_database():
    logger.info("Initializing database tables...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Check if menu already has items
        existing_count = db.query(MenuItem).count()
        if existing_count > 0:
            logger.info(f"Database already contains {existing_count} menu items. Skipping seed.")
            return

        logger.info("Seeding menu items...")
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
