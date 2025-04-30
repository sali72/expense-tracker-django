import json
from django.http import JsonResponse, HttpRequest
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from users.auth import get_user_id_from_request
from . import crud


@method_decorator(csrf_exempt, name="dispatch")
class ExpenseListView(View):
    async def get(self, request: HttpRequest) -> JsonResponse:
        """Get all expenses for the authenticated user"""
        # Authenticate request
        user_id = get_user_id_from_request(request)
        if not user_id:
            return JsonResponse({"detail": "Authentication failed"}, status=401)

        # Get all expenses
        expenses = await crud.get_all_expenses(user_id)

        # Serialize expenses
        expenses_data = crud.serialize_expenses(expenses)

        return JsonResponse(expenses_data, safe=False)

    async def post(self, request: HttpRequest) -> JsonResponse:
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

            # Create expense
            expense = await crud.create_expense(
                user_id=user_id, amount=amount, tag=tag, description=description
            )

            # Return created expense
            return JsonResponse(crud.serialize_expense(expense), status=201)

        except json.JSONDecodeError:
            return JsonResponse({"detail": "Invalid JSON"}, status=400)
        except Exception as e:
            print(type(e))
            return JsonResponse({"detail": str(e)}, status=400)


@method_decorator(csrf_exempt, name="dispatch")
class ExpenseDetailView(View):
    async def get(self, request: HttpRequest, expense_id: str) -> JsonResponse:
        """Get a specific expense"""
        # Authenticate request
        user_id = get_user_id_from_request(request)
        if not user_id:
            return JsonResponse({"detail": "Authentication failed"}, status=401)

        # Get expense
        expense = await crud.get_expense_by_id(expense_id, user_id)
        if not expense:
            return JsonResponse({"detail": "expense not found"}, status=404)

        # Return expense
        return JsonResponse(crud.serialize_expense(expense))

    async def patch(self, request: HttpRequest, expense_id: str) -> JsonResponse:
        """Update an expense"""
        # Authenticate request
        user_id = get_user_id_from_request(request)
        if not user_id:
            return JsonResponse({"detail": "Authentication failed"}, status=401)

        # Parse request data
        try:
            data = json.loads(request.body)

            # Update expense
            expense = await crud.update_expense(expense_id, user_id, data)
            if not expense:
                return JsonResponse({"detail": "expense not found"}, status=404)

            # Return updated expense
            return JsonResponse(crud.serialize_expense(expense))

        except json.JSONDecodeError:
            return JsonResponse({"detail": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"detail": str(e)}, status=400)

    async def delete(self, request: HttpRequest, expense_id: str) -> JsonResponse:
        """Delete an expense"""
        # Authenticate request
        user_id = get_user_id_from_request(request)
        if not user_id:
            return JsonResponse({"detail": "Authentication failed"}, status=401)

        # Delete expense
        expense = await crud.delete_expense(expense_id, user_id)
        if not expense:
            return JsonResponse({"detail": "expense not found"}, status=404)

        # Return deleted expense data
        return JsonResponse(crud.serialize_expense(expense))
