import json
import uuid
import pytest
from expenses.models import Expense


@pytest.fixture(scope="function", autouse=True)
async def clean_expenses_collection():
    """
    Clear the expenses collection before each test.
    """
    await Expense.find_all().delete()


@pytest.mark.asyncio
async def test_create_expense(client, test_user, auth_headers):
    """
    Test creating an expense.
    """
    data = {
        "amount": 100,
        "description": "Test expense",
        "tag": "food"
    }
    
    response = client.post(
        "/api/expenses/",
        data=json.dumps(data),
        content_type="application/json",
        **auth_headers
    )
    
    assert response.status_code == 201
    response_data = json.loads(response.content)
    assert response_data["amount"] == 100
    assert response_data["description"] == "Test expense"
    assert response_data["tag"] == "food"
    assert await Expense.find_all().count() == 1


@pytest.mark.asyncio
async def test_get_expenses(client, test_user, auth_headers):
    """
    Test getting all expenses for a user.
    """
    response = client.get("/api/expenses/", **auth_headers)
    
    assert response.status_code == 200
    response_data = json.loads(response.content)
    assert isinstance(response_data, list)
    assert len(response_data) == 0


@pytest.mark.asyncio
async def test_get_expenses_with_expenses(client, test_user, auth_headers):
    """
    Test getting all expenses for a user with existing expenses.
    """
    # Create an expense first
    data = {
        "amount": 100,
        "description": "Test expense",
        "tag": "food"
    }
    
    create_response = client.post(
        "/api/expenses/",
        data=json.dumps(data),
        content_type="application/json",
        **auth_headers
    )
    
    expense_id = json.loads(create_response.content)["id"]
    
    # Get all expenses
    response = client.get("/api/expenses/", **auth_headers)
    
    assert response.status_code == 200
    response_data = json.loads(response.content)
    assert isinstance(response_data, list)
    assert len(response_data) == 1
    assert response_data[0]["id"] == expense_id


@pytest.mark.asyncio
async def test_get_expense(client, test_user, auth_headers):
    """
    Test getting a specific expense.
    """
    # Create an expense first
    data = {
        "amount": 100,
        "description": "Test expense",
        "tag": "food"
    }
    
    create_response = client.post(
        "/api/expenses/",
        data=json.dumps(data),
        content_type="application/json",
        **auth_headers
    )
    
    expense_id = json.loads(create_response.content)["id"]
    
    # Get the expense
    response = client.get(f"/api/expenses/{expense_id}/", **auth_headers)
    
    assert response.status_code == 200
    response_data = json.loads(response.content)
    assert response_data["id"] == expense_id
    assert response_data["amount"] == 100
    assert response_data["description"] == "Test expense"


@pytest.mark.asyncio
async def test_get_nonexistent_expense(client, test_user, auth_headers):
    """
    Test getting an expense that doesn't exist.
    """
    random_uuid = str(uuid.uuid4())
    response = client.get(f"/api/expenses/{random_uuid}/", **auth_headers)
    
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_expense(client, test_user, auth_headers):
    """
    Test updating an expense.
    """
    # Create an expense first
    data = {
        "amount": 100,
        "description": "Test expense",
        "tag": "food"
    }
    
    create_response = client.post(
        "/api/expenses/",
        data=json.dumps(data),
        content_type="application/json",
        **auth_headers
    )
    
    expense_id = json.loads(create_response.content)["id"]
    
    # Update the expense
    update_data = {
        "amount": 200,
        "description": "Updated expense"
    }
    
    response = client.patch(
        f"/api/expenses/{expense_id}/",
        data=json.dumps(update_data),
        content_type="application/json",
        **auth_headers
    )
    
    assert response.status_code == 200
    response_data = json.loads(response.content)
    assert response_data["id"] == expense_id
    assert response_data["amount"] == 200
    assert response_data["description"] == "Updated expense"
    assert response_data["tag"] == "food"  # Should be unchanged


@pytest.mark.asyncio
async def test_update_nonexistent_expense(client, test_user, auth_headers):
    """
    Test updating an expense that doesn't exist.
    """
    random_uuid = str(uuid.uuid4())
    update_data = {
        "amount": 200
    }
    
    response = client.patch(
        f"/api/expenses/{random_uuid}/",
        data=json.dumps(update_data),
        content_type="application/json",
        **auth_headers
    )
    
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_expense(client, test_user, auth_headers):
    """
    Test deleting an expense.
    """
    # Create an expense first
    data = {
        "amount": 100,
        "description": "Test expense",
        "tag": "food"
    }
    
    create_response = client.post(
        "/api/expenses/",
        data=json.dumps(data),
        content_type="application/json",
        **auth_headers
    )
    
    expense_id = json.loads(create_response.content)["id"]
    
    # Delete the expense
    response = client.delete(f"/api/expenses/{expense_id}/", **auth_headers)
    
    assert response.status_code == 200
    response_data = json.loads(response.content)
    assert response_data["id"] == expense_id
    
    # Verify it's gone
    assert await Expense.find_all().count() == 0


@pytest.mark.asyncio
async def test_delete_nonexistent_expense(client, test_user, auth_headers):
    """
    Test deleting an expense that doesn't exist.
    """
    random_uuid = str(uuid.uuid4())
    response = client.delete(f"/api/expenses/{random_uuid}/", **auth_headers)
    
    assert response.status_code == 404 