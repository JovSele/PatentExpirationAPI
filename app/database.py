"""
Database connection and session management.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

# Create database engine
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,  # Verify connections before using
    pool_size=5,
    max_overflow=10,
    echo=settings.debug  # Log SQL queries in debug mode
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


def get_db():
    """
    Dependency function to get database session.
    Yields a database session and closes it after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# app/database.py

# ... (váš existujúci kód)

def check_db_connection():
    """
    Vytvorí a okamžite zatvorí spojenie, aby overil jeho funkčnosť.
    """
    try:
        # Použijeme SessionLocal, aby sme sa pokúsili otvoriť spojenie
        db = SessionLocal()
        # Najjednoduchší dotaz na svete na overenie funkčnosti
        db.execute("SELECT 1")
        return True
    except Exception as e:
        print(f"Database connection error: {e}") # Print, aby sme videli chybu v logoch Renderu
        return False
    finally:
        if 'db' in locals() and db:
            db.close()

def init_db():
    """
    Initialize database tables.
    Called on application startup.
    """
    Base.metadata.create_all(bind=engine)
