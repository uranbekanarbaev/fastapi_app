from tests.conftests import client
import pytest
from app import app
from db.schemas import StatusEnum  # Adjust this import based on your project structure

def create_user():
    """Helper function to create a test user."""
    response = client.post(
        "/users",
        data={"username": "testuser", "email": "test@example.com", "password": "password123"}
    )
    print("Create user response JSON:", response.json())  # Debugging line
    assert response.status_code == 200  # Check for success on user creation
    return response

def login_user(username, password):
    """Helper function to log in a test user and get the access token."""
    response = client.post(
        "/users",
        data={
            "username": username,
            "password": password,
            "email": "test@example.com"  # Include email if required
        }
    )
    print("Login response JSON:", response.json())  # Debugging line
    assert response.status_code == 200, f"Login failed with status code {response.status_code}"
    return response.cookies.get("access_token")  # Adjust this if your token is returned differently

@pytest.fixture
def auth_client():
    """Fixture to create an authenticated test client."""
    user_response = create_user()  # Create a test user
    user_data = user_response.json()

    # Use the username and password used in `create_user`
    token = login_user(user_data["user_data"]["username"], "password123")  # Make sure this password matches
    client.cookies.set("access_token", token)  # Set the cookie if that's how you're handling auth
    yield client
    client.cookies.clear()  # Clear cookies after tests

def test_create_task(auth_client):
    task_data = {
        "title": "my title",
        "description": "Test task description",
        "status": StatusEnum.in_process.value
    }
    
    print("Task data being sent:", task_data)  # Debugging line
    response = auth_client.post('/tasks', json=task_data)  # Use json instead of data
    
    # Print response details for debugging
    print("Response Status Code:", response.status_code)
    print("Response Content:", response.content)  # Print raw content
    
    assert response.status_code == 200
    assert "message" in response.json()

