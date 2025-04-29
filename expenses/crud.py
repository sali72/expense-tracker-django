from .models import Expense
from typing import List, Dict, Any, Optional, Union
from uuid import UUID


def get_expense_by_id(expense_id: Union[str, UUID], user_id: UUID) -> Optional[Expense]:
    """
    Get an expense by ID for a specific user.
    """
    try:
        if isinstance(expense_id, str):
            expense_id = UUID(expense_id)
        return Expense.objects.get(id=expense_id, user_id=user_id)
    except (ValueError, Expense.DoesNotExist):
        return None


def get_all_expenses(user_id: UUID) -> List[Expense]:
    """
    Get all expenses for a user.
    """
    return list(Expense.objects.filter(user_id=user_id))


def create_expense(
    user_id: UUID, amount: float, tag: str = None, description: str = None
) -> Expense:
    """
    Create a new expense for a user.
    """
    return Expense.objects.create(
        user_id=user_id, amount=amount, tag=tag, description=description
    )


def update_expense(
    expense_id: Union[str, UUID], user_id: UUID, data: Dict[str, Any]
) -> Optional[Expense]:
    """
    Update an expense with the provided data.
    """
    expense = get_expense_by_id(expense_id, user_id)
    if not expense:
        return None

    # Update fields if provided
    if "amount" in data:
        expense.amount = data["amount"]
    if "tag" in data:
        expense.tag = data["tag"]
    if "description" in data:
        expense.description = data["description"]

    expense.save()
    return expense


def delete_expense(expense_id: Union[str, UUID], user_id: UUID) -> Optional[Expense]:
    """
    Delete an expense. Returns the expense data if successful, None otherwise.
    """
    expense = get_expense_by_id(expense_id, user_id)
    if not expense:
        return None

    # Store expense data before deletion
    deleted_expense = expense
    expense.delete()
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
