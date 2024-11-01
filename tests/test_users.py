from tests.conftests import client

def test_create_user():
    response = client.post(
        "/users",
        data={"username": "testuser", "email": "test@example.com", "password": "password123"}
    )
    assert response.status_code == 200
    assert response.json()["user_data"]["username"] == "testuser"

def test_login_user():
    client.post(
        "/users",
        data={"username": "testuser", "email": "test@example.com", "password": "password123"}
    )
    
    response = client.post(
        "/token",
        data={"username": "testuser", "password": "password123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_get_user_by_id():
    user_response = client.post(
        "/users",
        data={"username": "user123", "email": "user123@example.com", "password": "password123"}
    )
    user_id = user_response.json()["user_data"]["id"]
    
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["username"] == "user123"