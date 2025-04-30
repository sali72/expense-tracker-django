import uuid
import pytest
import asyncio
from django.test import Client
from users.models import UserProfile
from expenses.models import Expense
from tests.utils import generate_test_access_token
from config.db import initialize_beanie


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def setup_beanie_db():
    """Initialize Beanie at the start of testing"""
    await initialize_beanie()


@pytest.fixture(scope="function")
def client():
    """Returns a Django test client."""
    return Client()


@pytest.fixture(scope="function")
async def clean_database():
    """Clear database between tests."""
    await Expense.find_all().delete()
    await UserProfile.find_all().delete()


@pytest.fixture(scope="session")
def user_id():
    """Generate a UUID for testing."""
    return uuid.uuid4()


@pytest.fixture(scope="session")
def token(user_id):
    """Generate a JWT token for a test user."""
    return generate_test_access_token(user_id)


@pytest.fixture(scope="session")
def auth_headers(token):
    """Return headers with authorization token."""
    return {"HTTP_AUTHORIZATION": f"Bearer {token}"}


@pytest.fixture(scope="function")
async def test_user(user_id):
    """Create a test user in the database."""
    user = UserProfile(id=user_id)
    await user.save()
    return user 