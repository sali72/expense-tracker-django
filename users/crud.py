from .models import UserProfile
from typing import Dict, Any, Optional, Union
from uuid import UUID


def get_user_by_id(user_id: Union[str, UUID]) -> Optional[UserProfile]:
    """
    Get a user by ID.
    """
    try:
        if isinstance(user_id, str):
            user_id = UUID(user_id)
        return UserProfile.objects.get(id=user_id)
    except (ValueError, UserProfile.DoesNotExist):
        return None


def create_user(user_id: Union[str, UUID]) -> Optional[UserProfile]:
    """
    Create a new user with the given ID.
    """
    try:
        if isinstance(user_id, str):
            user_id = UUID(user_id)

        # Check if user already exists
        if UserProfile.objects.filter(id=user_id).exists():
            return None

        # Create user
        return UserProfile.objects.create(id=user_id)
    except ValueError:
        return None


def delete_user(user_id: Union[str, UUID]) -> bool:
    """
    Delete a user. Returns True if successful, False otherwise.
    """
    user = get_user_by_id(user_id)
    if not user:
        return False

    user.delete()
    return True


def serialize_user(user: UserProfile) -> Dict[str, Any]:
    """
    Serialize a user object to a dictionary.
    """
    return {"id": str(user.id), "expense_ids": user.expense_ids}
