from typing import List
import uuid
from uuid import UUID
from beanie import Document
from pydantic import Field


class UserProfile(Document):
    """Document model for user profiles"""

    id: UUID = Field(default_factory=uuid.uuid4)
    expense_ids: List[str] = Field(default_factory=list)

    class Settings:
        name = "users"  # Collection name in MongoDB
        use_state_management = True

    class Config:
        arbitrary_types_allowed = True

    def __str__(self):
        """String representation of the user profile"""
        return str(self.id)
