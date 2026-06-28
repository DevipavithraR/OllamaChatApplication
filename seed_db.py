import logging
from app.database import SessionLocal, engine, Base
from app.models.Doctor import Doctor
from app.models.Department import Department

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("seed")

DEPARTMENTS = [
    {"department_name": "Cardiology", "description": "Heart related diagnosis and treatment."},
    {"department_name": "Pediatrics", "description": "Child healthcare."},
    {"department_name": "Orthopedics", "description": "Bone and joint treatment."},
    {"department_name": "Neurology", "description": "Brain and nervous system."},
    {"department_name": "General Medicine", "description": "General healthcare."}
]

DOCTORS = [
    {"name": "Dr. Priya", "department": "Cardiology", "specialization": "Cardiologist", "experience": 12, "consultation_fee": 700.00, "available_days": "Monday-Friday", "available_time": "10 AM-4 PM", "status": "ACTIVE"},
    {"name": "Dr. Sharma", "department": "Pediatrics", "specialization": "Pediatrician", "experience": 8, "consultation_fee": 500.00, "available_days": "Monday-Saturday", "available_time": "9 AM-1 PM", "status": "ACTIVE"},
    {"name": "Dr. Goel", "department": "Orthopedics", "specialization": "Orthopedic Surgeon", "experience": 15, "consultation_fee": 800.00, "available_days": "Tuesday-Thursday-Saturday", "available_time": "2 PM-6 PM", "status": "ACTIVE"},
    {"name": "Dr. Gupta", "department": "Neurology", "specialization": "Neurologist", "experience": 10, "consultation_fee": 900.00, "available_days": "Monday-Wednesday-Friday", "available_time": "11 AM-5 PM", "status": "ACTIVE"},
    {"name": "Dr. Verma", "department": "General Medicine", "specialization": "General Physician", "experience": 6, "consultation_fee": 400.00, "available_days": "Monday-Saturday", "available_time": "9 AM-5 PM", "status": "ACTIVE"}
]

def seed_database():
    logger.info("Initializing database tables...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Seed Departments
        existing_dept_count = db.query(Department).count()
        if existing_dept_count > 0:
            logger.info(f"Database already contains {existing_dept_count} departments. Skipping department seed.")
        else:
            logger.info("Seeding departments...")
            for dept_data in DEPARTMENTS:
                dept = Department(**dept_data)
                db.add(dept)
            db.commit()
            logger.info("Department seeding completed successfully!")

        # Seed Doctors
        existing_doc_count = db.query(Doctor).count()
        if existing_doc_count > 0:
            logger.info(f"Database already contains {existing_doc_count} doctors. Skipping doctor seed.")
        else:
            logger.info("Seeding doctors...")
            for doc_data in DOCTORS:
                doc = Doctor(**doc_data)
                db.add(doc)
            db.commit()
            logger.info("Doctor seeding completed successfully!")

    except Exception as e:
        db.rollback()
        logger.error(f"Error seeding database: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
