import logging
from datetime import date
from app.database import SessionLocal, engine, Base
from app.models.book import Book
from app.models.member import Member

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("seed")

BOOKS = [
    {
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "category": "Programming",
        "isbn": "978-0132350884",
        "publisher": "Prentice Hall",
        "publication_year": 2008,
        "available_copies": 5,
        "total_copies": 5,
        "description": "A handbook of agile software craftsmanship. Master the art of clean code."
    },
    {
        "title": "Introduction to Algorithms",
        "author": "Thomas H. Cormen",
        "category": "Computer Science",
        "isbn": "978-0262033848",
        "publisher": "MIT Press",
        "publication_year": 2009,
        "available_copies": 3,
        "total_copies": 3,
        "description": "A comprehensive design and analysis guide for algorithms."
    },
    {
        "title": "Design Patterns",
        "author": "Erich Gamma",
        "category": "Programming",
        "isbn": "978-0201633610",
        "publisher": "Addison-Wesley",
        "publication_year": 1994,
        "available_copies": 4,
        "total_copies": 4,
        "description": "Elements of Reusable Object-Oriented Software. The classic software engineering text."
    },
    {
        "title": "The Pragmatic Programmer",
        "author": "Andrew Hunt",
        "category": "Programming",
        "isbn": "978-0135957059",
        "publisher": "Addison-Wesley",
        "publication_year": 2019,
        "available_copies": 6,
        "total_copies": 6,
        "description": "Your journey to mastery. From journeyman to master."
    },
    {
        "title": "Artificial Intelligence: A Modern Approach",
        "author": "Stuart Russell",
        "category": "AI/ML",
        "isbn": "978-0136042594",
        "publisher": "Pearson",
        "publication_year": 2020,
        "available_copies": 2,
        "total_copies": 2,
        "description": "The reference textbook for AI studies worldwide."
    }
]

MEMBERS = [
    {
        "name": "Rahul Kumar",
        "phone_number": "+919876543210",
        "email": "rahul@example.com",
        "membership_type": "Premium",
        "registration_date": date(2026, 6, 1)
    },
    {
        "name": "Alice Smith",
        "phone_number": "+15550199",
        "email": "alice@example.com",
        "membership_type": "Regular",
        "registration_date": date(2026, 6, 15)
    }
]

def seed_database():
    logger.info("Initializing database tables...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Check if books already have items
        existing_books = db.query(Book).count()
        if existing_books == 0:
            logger.info("Seeding books...")
            for book_data in BOOKS:
                book = Book(**book_data)
                db.add(book)
            db.commit()
            logger.info("Books seeded successfully!")
        else:
            logger.info(f"Database already contains {existing_books} books. Skipping book seed.")

        # Check if members already have items
        existing_members = db.query(Member).count()
        if existing_members == 0:
            logger.info("Seeding members...")
            for member_data in MEMBERS:
                member = Member(**member_data)
                db.add(member)
            db.commit()
            logger.info("Members seeded successfully!")
        else:
            logger.info(f"Database already contains {existing_members} members. Skipping member seed.")

        logger.info("Seeding completed successfully!")
    except Exception as e:
        db.rollback()
        logger.error(f"Error seeding database: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
