"""
Test the retrieval of tasks from a protected route.

This test function performs the following steps:
1. Registers a new user with a username, email, and password.
2. Logs in with the registered user's credentials to obtain an access token.
3. Uses the access token to make a request to the protected '/tasks' endpoint.
4. Asserts that the response status code is 200, indicating successful access to the protected route.

This ensures that the authentication and authorization mechanisms are functioning as intended.
"""

from tests.conftests import client
import pytest
from logs.logger import logger

def test_get_tasks_protected(client):
    # Create a new user
    response = client.post(
        "/users",
        json={"username": "testuser2", "email": "test2@example.com", "password": "password123"}
    )
    assert response.status_code == 200

    # Log in with the new user
    login_response = client.post(
        "/login",
        json={"username": "testuser2", "password": "password123"}
    )

    logger.info(f'Received login response during the security test with following data: {login_response}')
    print(f'Received login response during the security test with following data: {login_response.json()}')

    assert login_response.status_code == 200
    access_token = login_response.json().get("access_token")
    assert access_token, "Access token not found in login response"

    response = client.get(
        "/tasks",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
