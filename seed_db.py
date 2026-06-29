import logging
from app.database import SessionLocal, engine, Base
from app.models.ServiceCatalog import ServiceCatalog
from app.models.Mechanic import Mechanic

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("seed")

SERVICES = [
    {"service_name": "General Service", "description": "Complete vehicle inspection, engine oil check & top up, filter cleaning, and basic electrical check.", "estimated_duration": "2 Hours", "service_cost": 2500.00},
    {"service_name": "Engine Repair", "description": "Advanced engine diagnostics, cylinder block overhaul, timing belt adjustments, and valve tuning.", "estimated_duration": "6 Hours", "service_cost": 8500.00},
    {"service_name": "Brake Replacement", "description": "Front and rear brake pad replacement, disc brake resurfacing, and brake fluid flushing.", "estimated_duration": "1.5 Hours", "service_cost": 1800.00},
    {"service_name": "AC Overhaul", "description": "AC compressor testing, condenser wash, evaporator cleaning, and refrigerant gas top-up.", "estimated_duration": "3 Hours", "service_cost": 3000.00},
    {"service_name": "Wheel Alignment", "description": "Precision wheel alignment, high-speed wheel balancing, tyre rotation, and tread health inspection.", "estimated_duration": "1 Hour", "service_cost": 1200.00}
]

MECHANICS = [
    {"name": "Arun Kumar", "specialization": "Engine Repair", "experience": 10, "available_status": "Available"},
    {"name": "Rajesh Sharma", "specialization": "Brake Replacement", "experience": 8, "available_status": "Available"},
    {"name": "Vikram Singh", "specialization": "AC Overhaul", "experience": 6, "available_status": "Available"},
    {"name": "Amit Patel", "specialization": "Wheel Alignment", "experience": 4, "available_status": "Available"},
    {"name": "Senthil Kumar", "specialization": "General Service", "experience": 5, "available_status": "Available"}
]

def seed_database():
    logger.info("Initializing database tables...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Check if services already seeded
        svc_count = db.query(ServiceCatalog).count()
        if svc_count == 0:
            logger.info("Seeding service catalog items...")
            for svc_data in SERVICES:
                svc = ServiceCatalog(**svc_data)
                db.add(svc)
            db.commit()
            logger.info("Seeding services completed successfully!")
        else:
            logger.info(f"Database already contains {svc_count} service catalog items. Skipping services seed.")

        # Check if mechanics already seeded
        mech_count = db.query(Mechanic).count()
        if mech_count == 0:
            logger.info("Seeding mechanics...")
            for mech_data in MECHANICS:
                mech = Mechanic(**mech_data)
                db.add(mech)
            db.commit()
            logger.info("Seeding mechanics completed successfully!")
        else:
            logger.info(f"Database already contains {mech_count} mechanics. Skipping mechanics seed.")
            
    except Exception as e:
        db.rollback()
        logger.error(f"Error seeding database: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
