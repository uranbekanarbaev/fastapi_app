"""
This module sets up the testing environment for the FastAPI application.

It configures a temporary SQLite database for testing purposes, allowing for 
isolation of tests without affecting the production database. The following 
components are included:

- A test database engine created using SQLAlchemy.
- A session local for interacting with the test database.
- An overridden dependency for FastAPI to use the test database session.
- Creation of the database tables defined in the application's models.
- A TestClient instance for making HTTP requests to the FastAPI app during tests.

Usage:
- This setup allows for running tests that require database interactions 
  without side effects on the main database.
"""


import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import app
from db.database import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

Base.metadata.create_all(bind=engine)

client = TestClient(app)
