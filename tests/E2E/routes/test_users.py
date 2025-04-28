import json
import uuid
import pytest
from django.test import Client
from users.models import UserProfile


@pytest.fixture(scope="function", autouse=True)
def clean_users_collection():
    """
    Clear the users collection before each test.
    """
    UserProfile.objects.all().delete()


@pytest.mark.django_db
def test_create_user(client):
    """
    Test creating a user.
    """
    user_id = str(uuid.uuid4())
    data = {
        "id": user_id
    }
    
    response = client.post(
        "/api/users/",
        data=json.dumps(data),
        content_type="application/json"
    )
    
    assert response.status_code == 201
    response_data = json.loads(response.content)
    assert response_data["id"] == user_id
    assert UserProfile.objects.count() == 1


@pytest.mark.django_db
def test_create_existing_user(client):
    """
    Test creating a user that already exists.
    """
    user_id = str(uuid.uuid4())
    
    # Create user first
    UserProfile.objects.create(id=user_id)
    
    # Try to create again
    data = {
        "id": user_id
    }
    
    response = client.post(
        "/api/users/",
        data=json.dumps(data),
        content_type="application/json"
    )
    
    assert response.status_code == 400
    assert "user already exists" in str(response.content)


@pytest.mark.django_db
def test_delete_user(client):
    """
    Test deleting a user.
    """
    user_id = str(uuid.uuid4())
    
    # Create user first
    UserProfile.objects.create(id=user_id)
    
    # Delete user
    response = client.delete(f"/api/users/?id={user_id}")
    
    assert response.status_code == 200
    response_data = json.loads(response.content)
    assert response_data["message"] == "user deleted"
    assert UserProfile.objects.count() == 0


@pytest.mark.django_db
def test_delete_nonexistent_user(client):
    """
    Test deleting a user that doesn't exist.
    """
    random_uuid = str(uuid.uuid4())
    response = client.delete(f"/api/users/?id={random_uuid}")
    
    assert response.status_code == 404
    assert "user not found" in str(response.content)


@pytest.mark.django_db
def test_auth_test(client, test_user, auth_headers):
    """
    Test the auth test endpoint.
    """
    response = client.get("/api/users/test-auth/", **auth_headers)
    
    assert response.status_code == 200
    response_data = json.loads(response.content)
    assert "Auth test successful" in response_data["message"] 