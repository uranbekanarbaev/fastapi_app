"""
Test Module for User Management API

This module contains unit tests for the user management endpoints of the FastAPI application.
It covers the following functionalities:

1. User Creation: Tests the endpoint for creating a new user.
2. User Login: Tests the login functionality and token retrieval.
3. User Retrieval: Tests fetching a user by their unique ID.

The tests utilize FastAPI's TestClient to simulate requests to the API and assert expected responses.

Usage:
    Run the tests using pytest. Ensure the test database is properly set up before running the tests.

Example:
    To run the tests, execute the following command in your terminal:
        pytest -v tests/test_user_management.py
"""


from tests.conftests import client

def test_create_user(client):
    response = client.post(
        "/users",
        json={"username": "testuser", "email": "test@example.com", "password": "password123"}
    )
    assert response.status_code == 200

def test_login_user(client):
    client.post(
        "/login",
        data={"username": "testuser", "email": "test@example.com", "password": "password123"}
    )
    
    response = client.post(
        "/token",
        data={"username": "testuser", "password": "password123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_get_user_by_id(client):
    user_response = client.post(
        "/users",
        data={"username": "user123", "email": "user123@example.com", "password": "password123"}
    )
    user_id = user_response.json()["user_data"]["id"]
    
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["username"] == "user123"