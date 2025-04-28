import json
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Expense
from users.auth import get_user_id_from_request
from uuid import UUID


@method_decorator(csrf_exempt, name='dispatch')
class ExpenseListView(View):
    def get(self, request) -> JsonResponse:
        """Get all expenses for the authenticated user"""
        # Authenticate request
        user_id = get_user_id_from_request(request)
        if not user_id:
            return JsonResponse({"detail": "Authentication failed"}, status=401)
            
        # Get all expenses for the user
        expenses = Expense.objects.filter(user_id=user_id)
        
        # Serialize expenses
        expenses_data = []
        for expense in expenses:
            expenses_data.append({
                'id': str(expense.id),
                'amount': expense.amount,
                'created_at': expense.created_at.isoformat(),
                'tag': expense.tag,
                'description': expense.description
            })
            
        return JsonResponse(expenses_data, safe=False)
    
    def post(self, request) -> JsonResponse:
        """Create a new expense"""
        # Authenticate request
        user_id = get_user_id_from_request(request)
        if not user_id:
            return JsonResponse({"detail": "Authentication failed"}, status=401)
            
        # Parse request data
        try:
            data = json.loads(request.body)
            amount = data.get('amount')
            tag = data.get('tag')
            description = data.get('description')
            
            # Validate required fields
            if amount is None:
                return JsonResponse({"detail": "amount is required"}, status=400)
                
            # Create expense
            expense = Expense.objects.create(
                user_id=user_id,
                amount=amount,
                tag=tag,
                description=description
            )
            
            # Return created expense
            return JsonResponse({
                'id': str(expense.id),
                'amount': expense.amount,
                'created_at': expense.created_at.isoformat(),
                'tag': expense.tag,
                'description': expense.description
            }, status=201)
            
        except json.JSONDecodeError:
            return JsonResponse({"detail": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"detail": str(e)}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class ExpenseDetailView(View):
    def get_object(self, expense_id, user_id):
        """Helper method to get expense by ID"""
        try:
            expense_id = UUID(expense_id)
            return Expense.objects.get(id=expense_id, user_id=user_id)
        except (ValueError, Expense.DoesNotExist):
            return None
    
    def get(self, request, expense_id) -> JsonResponse:
        """Get a specific expense"""
        # Authenticate request
        user_id = get_user_id_from_request(request)
        if not user_id:
            return JsonResponse({"detail": "Authentication failed"}, status=401)
            
        # Get expense
        expense = self.get_object(expense_id, user_id)
        if not expense:
            return JsonResponse({"detail": "expense not found"}, status=404)
            
        # Return expense
        return JsonResponse({
            'id': str(expense.id),
            'amount': expense.amount,
            'created_at': expense.created_at.isoformat(),
            'tag': expense.tag,
            'description': expense.description
        })

    def patch(self, request, expense_id) -> JsonResponse:
        """Update an expense"""
        # Authenticate request
        user_id = get_user_id_from_request(request)
        if not user_id:
            return JsonResponse({"detail": "Authentication failed"}, status=401)
            
        # Get expense
        expense = self.get_object(expense_id, user_id)
        if not expense:
            return JsonResponse({"detail": "expense not found"}, status=404)
            
        # Parse request data and update expense
        try:
            data = json.loads(request.body)
            
            # Update fields if provided
            if 'amount' in data:
                expense.amount = data['amount']
            if 'tag' in data:
                expense.tag = data['tag']
            if 'description' in data:
                expense.description = data['description']
                
            expense.save()
            
            # Return updated expense
            return JsonResponse({
                'id': str(expense.id),
                'amount': expense.amount,
                'created_at': expense.created_at.isoformat(),
                'tag': expense.tag,
                'description': expense.description
            })
            
        except json.JSONDecodeError:
            return JsonResponse({"detail": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"detail": str(e)}, status=400)
    
    def delete(self, request, expense_id) -> JsonResponse:
        """Delete an expense"""
        # Authenticate request
        user_id = get_user_id_from_request(request)
        if not user_id:
            return JsonResponse({"detail": "Authentication failed"}, status=401)
            
        # Get expense
        expense = self.get_object(expense_id, user_id)
        if not expense:
            return JsonResponse({"detail": "expense not found"}, status=404)
            
        # Prepare response data before deleting
        expense_data = {
            'id': str(expense.id),
            'amount': expense.amount,
            'created_at': expense.created_at.isoformat(),
            'tag': expense.tag,
            'description': expense.description
        }
        
        # Delete expense
        expense.delete()
        
        # Return deleted expense data
        return JsonResponse(expense_data)
