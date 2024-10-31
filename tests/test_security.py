from tests.conftests import client

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
    access_token = login_response.json()["access_token"]
    
    # Test access to a protected route
    response = client.get(
        "/tasks",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
