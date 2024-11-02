"""
Database module.

This module sets up a connection to a SQLite database, creates a session,
and provides functionality for interacting with the database in the application.

Functions:
- get_db: Creates and returns a new database session.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

Base.metadata.create_all(bind=engine)

def get_db():
    """Create a new database session and yield it.

    This function provides a database session for use in FastAPI route
    handlers. It ensures that the session is properly closed after use.

    Yields:
        Session: A SQLAlchemy session for interacting with the database.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()