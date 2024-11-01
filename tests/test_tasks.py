from tests.conftests import client
import pytest
from app import app
from db.schemas import StatusEnum

def create_user():
    """Helper function to create a test user."""
    response = client.post(
        "/users",
        data={"username": "testuser", "email": "test@example.com", "password": "password123"}
    )
    print("Create user response JSON:", response.json())
    assert response.status_code == 200
    return response

def login_user(username, password):
    """Helper function to log in a test user and get the access token."""
    response = client.post(
        "/users",
        data={
            "username": username,
            "password": password,
            "email": "test@example.com"
        }
    )
    print("Login response JSON:", response.json())
    assert response.status_code == 200, f"Login failed with status code {response.status_code}"
    return response.cookies.get("access_token")

@pytest.fixture
def auth_client():
    """Fixture to create an authenticated test client."""
    user_response = create_user()
    user_data = user_response.json()

    token = login_user(user_data["user_data"]["username"], "password123")
    client.cookies.set("access_token", token)
    yield client
    client.cookies.clear()

def test_create_task(auth_client):
    task_data = {
        "title": "my title",
        "description": "Test task description",
        "status": StatusEnum.in_process.value
    }
    
    print("Task data being sent:", task_data)
    response = auth_client.post('/tasks', json=task_data)
    
    print("Response Status Code:", response.status_code)
    print("Response Content:", response.content)
    
    assert response.status_code == 200
    assert "message" in response.json()

