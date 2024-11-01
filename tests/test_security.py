from tests.conftests import client
import pytest

@pytest.fixture(autouse=True)
def cleanup_users():
    """Cleanup users after each test."""
    yield
    # Code to remove the test user goes here
    client.delete("/users/testuser2")

def test_get_tasks_protected():
    # Register and login to obtain token
    client.post(
        "/users",
        data={"username": "testuser2", "email": "test2@example.com", "password": "password123"}
    )
    login_response = client.post(
        "/token",
        data={"username": "testuser2", "password": "password123"}
    )
    assert login_response.status_code == 200  # Ensure login was successful
    access_token = login_response.json()["access_token"]
    
    # Test access to a protected route
    response = client.get(
        "/tasks",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Check if response is a list
    # Additional assertions can be added here to check the structure of tasks
