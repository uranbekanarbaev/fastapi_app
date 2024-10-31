import pytest
from fastapi.testclient import TestClient
from app import app  # Ensure this path is correct to where FastAPI app is defined
from db.models import User  # Adjust based on the location of your User model
from loggs.logger import logger
from functools import wraps
import uuid

client = TestClient(app)

def create_and_delete_user(func):
    @wraps(func)
    def wrapper():
        sample_user = create_sample_user()
        try:
            result = func(sample_user)
        finally:
            delete_sample_user(sample_user.json()["user_data"]["id"])
        return result
    return wrapper


def create_sample_user():
    """Helper function to create a test user"""
    data = {
        "username": f"JohnDoe_{uuid.uuid4().hex[:6]}",
        "email": f"test_{uuid.uuid4().hex[:6]}@example.com",
        "password": "securepassword123"
    }
    response = client.post('/users', data=data)  # Use `json` for proper payload formatting
    return response

def delete_sample_user(user_id):
    client.delete(f'/users/{user_id}')

# Test creating a user
@create_and_delete_user
def test_create_user(sample_user):
    assert sample_user.status_code == 200
    assert "user_data" in sample_user.json()
    assert sample_user.json()["user_data"]["username"].startswith("JohnDoe_")

@create_and_delete_user
def test_get_user(response):
    user_id = response.json()["user_data"]["id"]
    get_response = client.get(f'/users/{user_id}')
    assert get_response.status_code == 200
    assert get_response.json()["username"] == "JohnDoe"

# Test updating a user
@create_and_delete_user
def test_update_user(response):
    user_id = response.json()["user_data"]["id"]
    updated_data = {
        "username": "UpdatedUser",
        "email": "updated@example.com",
    }
    response = client.put(f'/users/{user_id}', data=updated_data)
    assert response.status_code == 200
    assert response.json()["username"] == "UpdatedUser"

# Test deleting a user
def test_user_delete():
    user = create_sample_user()
    user_id = user.json()["user_data"]["id"]
    del_response = client.delete(f'/users/{user_id}')
    assert del_response.status_code == 200
    # Check user no longer exists
    get_response = client.get(f'/users/{user_id}')
    assert get_response.status_code == 404

# Test retrieving tasks for a user
@create_and_delete_user
def test_get_tasks(response):
    response = create_sample_user()
    response = client.get('/tasks')
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# Test retrieving a specific task
@create_and_delete_user
def test_get_specific_task(response):
    task_data = {"description": "Sample task"}
    response = client.post('/tasks', data=task_data)
    task_id = response.json()["id"]
    get_response = client.get(f'/tasks/{task_id}')
    assert get_response.status_code == 200
    assert get_response.json()["description"] == "Sample task"

# Test updating a task
@create_and_delete_user
def test_update_task(response):
    task_data = {"description": "Initial task"}
    task = client.post('/tasks', data=task_data)
    task_id = task.json()["id"]
    updated_task_data = {"name": "Updated Task", "description": "Updated description", "status": True}
    response = client.put(f'/tasks/{task_id}', data=updated_task_data)
    assert response.status_code == 200
    assert response.json()["description"] == "Updated description"

# Test deleting a task
@create_and_delete_user
def test_delete_task(response):
    task_data = {"description": "Task to delete"}
    task = client.post('/tasks', data=task_data)
    task_id = task.json()["id"]
    del_response = client.delete(f'/tasks/{task_id}')
    assert del_response.status_code == 200
    # Confirm task no longer exists
    get_response = client.get(f'/tasks/{task_id}')
    assert get_response.status_code == 404

# Test protected route requires authentication
def test_protected_route():
    response = client.get('/tasks')  # without auth header
    assert response.status_code == 401  # Unauthorized if not authenticated

# Test performance (e.g., checking response time under 200ms for creating user)
def test_performance():
    import time
    start_time = time.time()
    response = create_sample_user()
    end_time = time.time()
    assert end_time - start_time < 0.2  # 200 ms threshold
    assert response.status_code == 200

# Test creating user with invalid data (missing fields)
def test_create_user_invalid_data():
    response = client.post('/users', data={"username": "InvalidUser"})
    assert response.status_code == 422  # Unprocessable Entity for missing fields

# Test for potential SQL injection vulnerability
def test_sql_injection():
    data = {
        "username": "' OR 1=1; --",
        "email": "injection_test@example.com",
        "password": "password123"
    }
    response = client.post('/users', json=data)
    assert response.status_code == 400  # SQL injection attempt should fail

# Cookie handling and reading
def test_set_and_read_cookie():
    response = client.post('/set-cookies')
    assert response.cookies.get('fakesession123') == "fake123-cookie-session-value"
    read_cookie_response = client.get('/read-cookie')
    assert read_cookie_response.status_code == 400  # Should be missing cookie 'access_token'
