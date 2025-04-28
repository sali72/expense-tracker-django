import uuid
import pytest
from django.test import Client
from users.models import UserProfile
from tests.utils import generate_test_access_token


@pytest.fixture(scope="session")
def test_db():
    """
    Create a test database and clean it up after tests complete.
    """
    return None  # Django handles test database automatically


@pytest.fixture(scope="function")
def client():
    """
    Returns a Django test client.
    """
    return Client()


@pytest.fixture(scope="function", autouse=True)
def clean_database():
    """
    Clear database between tests.
    """
    from expenses.models import Expense
    from users.models import UserProfile
    
    Expense.objects.all().delete()
    UserProfile.objects.all().delete()


@pytest.fixture(scope="session")
def user_id():
    """
    Generate a UUID for testing.
    """
    return uuid.uuid4()


@pytest.fixture(scope="session")
def token(user_id):
    """
    Generate a JWT token for a test user.
    """
    return generate_test_access_token(user_id)


@pytest.fixture(scope="session")
def auth_headers(token):
    """
    Return headers with authorization token.
    """
    return {"HTTP_AUTHORIZATION": f"Bearer {token}"}


@pytest.fixture(scope="function")
def test_user(user_id):
    """
    Create a test user in the database.
    """
    user = UserProfile.objects.create(id=user_id)
    return user 