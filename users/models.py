import uuid
from django.db import models

# Create your models here.

class UserProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    expense_ids = models.JSONField(default=list, help_text="List of user's expense IDs")

    def __str__(self):
        return str(self.id)
