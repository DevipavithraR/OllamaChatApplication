import logging
from app.database import SessionLocal, engine, Base
from app.models.MembershipPlan import MembershipPlan
from app.models.Trainer import Trainer

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("seed")

MEMBERSHIP_PLANS = [
    {
        "plan_name": "Gold Membership",
        "duration": "12 Months",
        "price": 18000.00,
        "benefits": "Unlimited Gym Access, Personal Diet Plan, Group Classes",
        "description": "All-access premium pass to the gym and group activities."
    },
    {
        "plan_name": "Silver Membership",
        "duration": "6 Months",
        "price": 10000.00,
        "benefits": "Unlimited Gym Access, Group Classes",
        "description": "Standard pass covering basic facilities and group workouts."
    },
    {
        "plan_name": "Platinum Membership",
        "duration": "12 Months",
        "price": 25000.00,
        "benefits": "Unlimited Gym Access, Personal Diet Plan, Group Classes, 1-on-1 Personal Trainer",
        "description": "Ultimate pass with full training support and personalized guidance."
    }
]

TRAINERS = [
    {
        "trainer_name": "Rahul Sharma",
        "specialization": "Weight Loss, Strength Training",
        "experience": "8 Years",
        "available_days": "Monday-Friday",
        "available_time": "6:00 AM - 2:00 PM",
        "session_fee": 600.00,
        "status": "ACTIVE"
    },
    {
        "trainer_name": "Priya Patel",
        "specialization": "Yoga, Pilates, Flexibility",
        "experience": "5 Years",
        "available_days": "Monday-Saturday",
        "available_time": "7:00 AM - 12:00 PM",
        "session_fee": 500.00,
        "status": "ACTIVE"
    },
    {
        "trainer_name": "Vikram Singh",
        "specialization": "Bodybuilding, Strength & Conditioning",
        "experience": "10 Years",
        "available_days": "Monday, Wednesday, Friday",
        "available_time": "2:00 PM - 8:00 PM",
        "session_fee": 800.00,
        "status": "ACTIVE"
    }
]

def seed_database():
    logger.info("Initializing database tables...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Seed Membership Plans
        logger.info("Seeding membership plans...")
        for plan_data in MEMBERSHIP_PLANS:
            plan = db.query(MembershipPlan).filter(MembershipPlan.plan_name == plan_data["plan_name"]).first()
            if not plan:
                plan = MembershipPlan(**plan_data)
                db.add(plan)
            else:
                for key, val in plan_data.items():
                    setattr(plan, key, val)
        
        # Seed Trainers
        logger.info("Seeding trainers...")
        for trainer_data in TRAINERS:
            trainer = db.query(Trainer).filter(Trainer.trainer_name == trainer_data["trainer_name"]).first()
            if not trainer:
                trainer = Trainer(**trainer_data)
                db.add(trainer)
            else:
                for key, val in trainer_data.items():
                    setattr(trainer, key, val)
                    
        db.commit()
        logger.info("Seeding completed successfully!")
    except Exception as e:
        db.rollback()
        logger.error(f"Error seeding database: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
