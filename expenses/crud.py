from typing import List, Dict, Any, Optional, Union
from uuid import UUID
from .models import Expense


async def get_expense_by_id(
    expense_id: Union[str, UUID], user_id: Union[str, UUID]
) -> Optional[Expense]:
    """
    Get an expense by ID for a specific user.
    """
    try:
        # Convert string IDs to UUID if needed
        if isinstance(expense_id, str):
            expense_id = UUID(expense_id)
        if isinstance(user_id, str):
            user_id = UUID(user_id)

        # Query using Beanie
        return await Expense.find_one({"id": expense_id, "user_id": user_id})
    except (ValueError, Exception):
        return None


async def get_all_expenses(user_id: Union[str, UUID]) -> List[Expense]:
    """
    Get all expenses for a user.
    """
    if isinstance(user_id, str):
        try:
            user_id = UUID(user_id)
        except ValueError:
            return []

    # Query using Beanie and convert to list
    expenses = await Expense.find({"user_id": user_id}).sort("-created_at").to_list()
    return expenses


async def create_expense(
    user_id: Union[str, UUID], amount: float, tag: str = None, description: str = None
) -> Expense:
    """
    Create a new expense for a user.
    """
    # Convert string ID to UUID if needed
    if isinstance(user_id, str):
        user_id = UUID(user_id)

    # Create new Expense document
    expense = Expense(amount=amount, tag=tag, description=description, user_id=user_id)

    # Save to database
    await expense.save()
    return expense


async def update_expense(
    expense_id: Union[str, UUID], user_id: Union[str, UUID], data: Dict[str, Any]
) -> Optional[Expense]:
    """
    Update an expense with the provided data.
    """
    # Get the expense
    expense = await get_expense_by_id(expense_id, user_id)
    if not expense:
        return None

    # Update fields
    if "amount" in data:
        expense.amount = data["amount"]
    if "tag" in data:
        expense.tag = data["tag"]
    if "description" in data:
        expense.description = data["description"]

    # Save changes
    await expense.save()
    return expense


async def delete_expense(
    expense_id: Union[str, UUID], user_id: Union[str, UUID]
) -> Optional[Expense]:
    """
    Delete an expense. Returns the expense data if successful, None otherwise.
    """
    # Get the expense
    expense = await get_expense_by_id(expense_id, user_id)
    if not expense:
        return None

    # Store expense for return value
    deleted_expense = expense

    # Delete from database
    await expense.delete()
    return deleted_expense


def serialize_expense(expense: Expense) -> Dict[str, Any]:
    """
    Serialize an expense object to a dictionary.
    """
    return {
        "id": str(expense.id),
        "amount": expense.amount,
        "created_at": expense.created_at.isoformat(),
        "tag": expense.tag,
        "description": expense.description,
    }


def serialize_expenses(expenses: List[Expense]) -> List[Dict[str, Any]]:
    """
    Serialize a list of expense objects.
    """
    return [serialize_expense(expense) for expense in expenses]
