import uuid
from django.db import models


class ExpenseTag(models.TextChoices):
    FOOD = 'food', 'Food'
    TRANSPORTATION = 'transportation', 'Transportation'
    TRAVEL = 'travel', 'Travel'
    ENTERTAINMENT = 'entertainment', 'Entertainment'
    GROCERIES = 'groceries', 'Groceries'
    LEISURE = 'leisure', 'Leisure'
    ELECTRONICS = 'electronics', 'Electronics'
    UTILITIES = 'utilities', 'Utilities'
    CLOTHING = 'clothing', 'Clothing'
    HEALTH = 'health', 'Health'
    OTHER = 'other', 'Other'


class Expense(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    tag = models.CharField(
        max_length=20,
        choices=ExpenseTag.choices,
        default=ExpenseTag.OTHER
    )
    description = models.TextField(blank=True, null=True)
    user_id = models.UUIDField()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.amount} - {self.tag} - {self.created_at.strftime('%Y-%m-%d')}"
