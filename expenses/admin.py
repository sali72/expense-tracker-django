from django.contrib import admin
from .models import Expense

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount', 'tag', 'created_at', 'user_id')
    list_filter = ('tag', 'created_at')
    search_fields = ('description', 'tag')
