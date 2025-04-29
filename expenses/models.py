from typing import Optional
from datetime import datetime
import uuid
from uuid import UUID
from beanie import Document
from pydantic import Field


class ExpenseTag:
    """Tags for expense categorization"""

    FOOD = "food"
    TRANSPORTATION = "transportation"
    TRAVEL = "travel"
    ENTERTAINMENT = "entertainment"
    GROCERIES = "groceries"
    LEISURE = "leisure"
    ELECTRONICS = "electronics"
    UTILITIES = "utilities"
    CLOTHING = "clothing"
    HEALTH = "health"
    OTHER = "other"

    CHOICES = [
        FOOD,
        TRANSPORTATION,
        TRAVEL,
        ENTERTAINMENT,
        GROCERIES,
        LEISURE,
        ELECTRONICS,
        UTILITIES,
        CLOTHING,
        HEALTH,
        OTHER,
    ]


class Expense(Document):
    """Document model for expenses"""

    id: UUID = Field(default_factory=uuid.uuid4)
    amount: float
    created_at: datetime = Field(default_factory=datetime.utcnow)
    tag: str = ExpenseTag.OTHER
    description: Optional[str] = None
    user_id: UUID

    class Settings:
        name = "expenses"  # Collection name in MongoDB
        use_state_management = True

    class Config:
        arbitrary_types_allowed = True

    def __str__(self):
        """String representation of the expense"""
        return f"{self.amount} - {self.tag} - {self.created_at.strftime('%Y-%m-%d')}"
