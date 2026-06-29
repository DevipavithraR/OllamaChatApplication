import logging
from datetime import datetime
from app.database import SessionLocal, engine, Base
from app.models.Movie import Movie
from app.models.Theatre import Theatre
from app.models.Show import Show

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("seed")

MOVIES = [
    {"title": "Interstellar", "genre": "Sci-Fi", "language": "English", "duration": "169 Minutes", "rating": "PG-13", "description": "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.", "release_date": datetime.strptime("2014-11-07", "%Y-%m-%d").date()},
    {"title": "Inception", "genre": "Sci-Fi", "language": "English", "duration": "148 Minutes", "rating": "PG-13", "description": "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea.", "release_date": datetime.strptime("2010-07-16", "%Y-%m-%d").date()},
    {"title": "The Dark Knight", "genre": "Action", "language": "English", "duration": "152 Minutes", "rating": "PG-13", "description": "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests.", "release_date": datetime.strptime("2008-07-18", "%Y-%m-%d").date()}
]

THEATRES = [
    {"theatre_name": "PVR Cinemas", "location": "Mall of India, Sector 18", "screens": 4},
    {"theatre_name": "IMAX Theatre", "location": "Forum Mall, Koramangala", "screens": 2}
]

SHOWS = [
    {
        "movie_title": "Interstellar",
        "theatre_name": "PVR Cinemas",
        "screen_number": 2,
        "show_datetime": datetime.strptime("2026-07-20 19:30:00", "%Y-%m-%d %H:%M:%S"),
        "ticket_price": 250.00,
        "available_seats": 42,
        "total_seats": 50
    },
    {
        "movie_title": "Inception",
        "theatre_name": "PVR Cinemas",
        "screen_number": 1,
        "show_datetime": datetime.strptime("2026-07-20 14:00:00", "%Y-%m-%d %H:%M:%S"),
        "ticket_price": 200.00,
        "available_seats": 50,
        "total_seats": 50
    },
    {
        "movie_title": "Interstellar",
        "theatre_name": "IMAX Theatre",
        "screen_number": 1,
        "show_datetime": datetime.strptime("2026-07-21 18:00:00", "%Y-%m-%d %H:%M:%S"),
        "ticket_price": 400.00,
        "available_seats": 35,
        "total_seats": 40
    }
]

def seed_database():
    logger.info("Initializing database tables...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Seed Movies
        existing_movie_count = db.query(Movie).count()
        if existing_movie_count > 0:
            logger.info(f"Database already contains {existing_movie_count} movies. Skipping movie seed.")
        else:
            logger.info("Seeding movies...")
            for m_data in MOVIES:
                movie = Movie(**m_data)
                db.add(movie)
            db.commit()
            logger.info("Movie seeding completed successfully!")

        # Seed Theatres
        existing_theatre_count = db.query(Theatre).count()
        if existing_theatre_count > 0:
            logger.info(f"Database already contains {existing_theatre_count} theatres. Skipping theatre seed.")
        else:
            logger.info("Seeding theatres...")
            for t_data in THEATRES:
                theatre = Theatre(**t_data)
                db.add(theatre)
            db.commit()
            logger.info("Theatre seeding completed successfully!")

        # Seed Shows
        existing_show_count = db.query(Show).count()
        if existing_show_count > 0:
            logger.info(f"Database already contains {existing_show_count} shows. Skipping show seed.")
        else:
            logger.info("Seeding shows...")
            movies = db.query(Movie).all()
            movie_map = {m.title: m.movie_id for m in movies}

            theatres = db.query(Theatre).all()
            theatre_map = {t.theatre_name: t.theatre_id for t in theatres}

            for s_data in SHOWS:
                movie_title = s_data.pop("movie_title")
                theatre_name = s_data.pop("theatre_name")

                s_data["movie_id"] = movie_map[movie_title]
                s_data["theatre_id"] = theatre_map[theatre_name]

                show = Show(**s_data)
                db.add(show)
            db.commit()
            logger.info("Show seeding completed successfully!")

    except Exception as e:
        db.rollback()
        logger.error(f"Error seeding database: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
