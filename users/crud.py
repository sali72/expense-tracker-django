from typing import Dict, Any, Optional, Union
from uuid import UUID
from .models import UserProfile


async def get_user_by_id(user_id: Union[str, UUID]) -> Optional[UserProfile]:
    """
    Get a user by ID.
    """
    try:
        # Convert string ID to UUID if needed
        if isinstance(user_id, str):
            user_id = UUID(user_id)

        # Query using Beanie
        return await UserProfile.find_one({"id": user_id})
    except (ValueError, Exception):
        return None


async def create_user(user_id: Union[str, UUID]) -> Optional[UserProfile]:
    """
    Create a new user with the given ID.
    """
    try:
        # Convert string ID to UUID if needed
        if isinstance(user_id, str):
            user_id = UUID(user_id)

        # Check if user already exists
        existing_user = await UserProfile.find_one({"id": user_id})
        if existing_user:
            return None

        # Create new UserProfile document
        user = UserProfile(id=user_id)

        # Save to database
        await user.save()
        return user
    except (ValueError, Exception):
        return None


async def delete_user(user_id: Union[str, UUID]) -> bool:
    """
    Delete a user. Returns True if successful, False otherwise.
    """
    # Get the user
    user = await get_user_by_id(user_id)
    if not user:
        return False

    # Delete from database
    await user.delete()
    return True


def serialize_user(user: UserProfile) -> Dict[str, Any]:
    """
    Serialize a user object to a dictionary.
    """
    return {"id": str(user.id), "expense_ids": user.expense_ids}
