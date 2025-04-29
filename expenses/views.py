import json
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from users.auth import get_user_id_from_request
from . import crud


@method_decorator(csrf_exempt, name="dispatch")
class ExpenseListView(View):
    def get(self, request) -> JsonResponse:
        """Get all expenses for the authenticated user"""
        # Authenticate request
        user_id = get_user_id_from_request(request)
        if not user_id:
            return JsonResponse({"detail": "Authentication failed"}, status=401)

        # Get all expenses using the repository
        expenses = crud.get_all_expenses(user_id)

        # Serialize expenses using the repository
        expenses_data = crud.serialize_expenses(expenses)

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
            amount = data.get("amount")
            tag = data.get("tag")
            description = data.get("description")

            # Validate required fields
            if amount is None:
                return JsonResponse({"detail": "amount is required"}, status=400)

            # Create expense using the repository
            expense = crud.create_expense(
                user_id=user_id, amount=amount, tag=tag, description=description
            )

            # Return created expense
            return JsonResponse(crud.serialize_expense(expense), status=201)

        except json.JSONDecodeError:
            return JsonResponse({"detail": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"detail": str(e)}, status=400)


@method_decorator(csrf_exempt, name="dispatch")
class ExpenseDetailView(View):
    def get(self, request, expense_id) -> JsonResponse:
        """Get a specific expense"""
        # Authenticate request
        user_id = get_user_id_from_request(request)
        if not user_id:
            return JsonResponse({"detail": "Authentication failed"}, status=401)

        # Get expense using the repository
        expense = crud.get_expense_by_id(expense_id, user_id)
        if not expense:
            return JsonResponse({"detail": "expense not found"}, status=404)

        # Return expense using the repository serializer
        return JsonResponse(crud.serialize_expense(expense))

    def patch(self, request, expense_id) -> JsonResponse:
        """Update an expense"""
        # Authenticate request
        user_id = get_user_id_from_request(request)
        if not user_id:
            return JsonResponse({"detail": "Authentication failed"}, status=401)

        # Parse request data
        try:
            data = json.loads(request.body)

            # Update expense using the repository
            expense = crud.update_expense(expense_id, user_id, data)
            if not expense:
                return JsonResponse({"detail": "expense not found"}, status=404)

            # Return updated expense
            return JsonResponse(crud.serialize_expense(expense))

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

        # Delete expense using the repository
        expense = crud.delete_expense(expense_id, user_id)
        if not expense:
            return JsonResponse({"detail": "expense not found"}, status=404)

        # Return deleted expense data
        return JsonResponse(crud.serialize_expense(expense))
