import json
from django.http import JsonResponse, HttpRequest
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.utils.decorators import async_to_sync
from users.auth import get_user_id_from_request
from . import crud
from config.db import initialize_beanie


class AsyncView(View):
    """Base class for async views"""

    async def dispatch_async(self, request, *args, **kwargs):
        """Async dispatch method to be implemented by subclasses"""
        handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        return await handler(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        """Synchronous dispatch that calls the async dispatch"""

        # Initialize Beanie if needed
        async def initialize():
            await initialize_beanie()

        # Only initialize once
        if not hasattr(self.__class__, "_beanie_initialized"):
            async_to_sync(initialize)()
            self.__class__._beanie_initialized = True

        # Call the async dispatch method
        return async_to_sync(self.dispatch_async)(request, *args, **kwargs)


@method_decorator(csrf_exempt, name="dispatch")
class ExpenseListView(AsyncView):
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
            return JsonResponse({"detail": str(e)}, status=400)


@method_decorator(csrf_exempt, name="dispatch")
class ExpenseDetailView(AsyncView):
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
