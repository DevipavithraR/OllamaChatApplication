import logging
from app.database import SessionLocal, engine, Base
from app.models.Course import Course
from app.models.Department import Department

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("seed")

DEPARTMENTS = [
    {"department_name": "Computer Science Department", "description": "Focuses on AI, Cloud Computing, Software Development and Data Science.", "head_of_department": "Dr. Alan Turing"},
    {"department_name": "Electronics & Communication Department", "description": "Covers core hardware, embedded devices, and communication networks.", "head_of_department": "Dr. Claude Shannon"},
    {"department_name": "Information Technology Department", "description": "Studies web development, software engineering, databases, and networks.", "head_of_department": "Dr. Tim Berners-Lee"},
    {"department_name": "Mechanical Engineering Department", "description": "Deals with designs, thermal engineering, robotics, and production.", "head_of_department": "Dr. James Watt"}
]

COURSES = [
    {
        "course_name": "B.Tech Computer Science",
        "department_id": 1,
        "duration": "4 Years",
        "total_seats": 30,
        "available_seats": 25,
        "fees": 85000.00,
        "eligibility": "Minimum 60%",
        "description": "Focuses on core programming, machine learning, systems architecture and algorithmic theory."
    },
    {
        "course_name": "B.Tech Data Science",
        "department_id": 1,
        "duration": "4 Years",
        "total_seats": 25,
        "available_seats": 22,
        "fees": 90000.00,
        "eligibility": "Minimum 65%",
        "description": "Learn modern big data ingestion, statistics, data analytics and machine learning."
    },
    {
        "course_name": "B.Tech Electronics & Comm.",
        "department_id": 2,
        "duration": "4 Years",
        "total_seats": 20,
        "available_seats": 18,
        "fees": 80000.00,
        "eligibility": "Minimum 55%",
        "description": "Comprehensive study of semiconductor devices, RF communication, VLSI, and signal processing."
    },
    {
        "course_name": "M.Tech Software Engineering",
        "department_id": 3,
        "duration": "2 Years",
        "total_seats": 15,
        "available_seats": 12,
        "fees": 110000.00,
        "eligibility": "Minimum 65%",
        "description": "Advanced system architecture, software quality controls, DevOps, and project management."
    }
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

        # Seed Courses
        existing_course_count = db.query(Course).count()
        if existing_course_count > 0:
            logger.info(f"Database already contains {existing_course_count} courses. Skipping course seed.")
        else:
            logger.info("Seeding courses...")
            # Query departments to map the seeded department IDs correctly
            departments = db.query(Department).all()
            dept_map = {d.department_name: d.department_id for d in departments}

            for course_data in COURSES:
                # Find matching dept ID
                dept_name = None
                if course_data["department_id"] == 1:
                    dept_name = "Computer Science Department"
                elif course_data["department_id"] == 2:
                    dept_name = "Electronics & Communication Department"
                elif course_data["department_id"] == 3:
                    dept_name = "Information Technology Department"
                elif course_data["department_id"] == 4:
                    dept_name = "Mechanical Engineering Department"
                
                if dept_name and dept_name in dept_map:
                    course_data["department_id"] = dept_map[dept_name]
                
                course = Course(**course_data)
                db.add(course)
            db.commit()
            logger.info("Course seeding completed successfully!")

    except Exception as e:
        db.rollback()
        logger.error(f"Error seeding database: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
