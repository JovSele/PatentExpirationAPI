"""
Database connection and session management.
"""

from sqlalchemy import create_engine, text 
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
    Pokúsi sa otvoriť session a spustiť SELECT 1, aby overil pripojenie.
    Vráti string 'connected' alebo 'disconnected'.
    """
    db = None
    try:
        db = SessionLocal()
        # OPRAVA: Obalenie SQL stringu funkciou text() pre SQLAlchemy 2.0
        db.execute(text("SELECT 1")) 
        return "connected"
    except Exception as e:
        print(f"Database connection check failed: {e}")
        return "disconnected"
    finally:
        if db:
            db.close()

def init_db():
    """
    Initialize database tables.
    Called on application startup.
    """
    Base.metadata.create_all(bind=engine)
