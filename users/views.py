import json
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .auth import get_user_id_from_request
from . import crud


@method_decorator(csrf_exempt, name="dispatch")
class TestAuthView(View):
    def get(self, request):
        """Test authentication endpoint"""
        user_id = get_user_id_from_request(request)
        if not user_id:
            return JsonResponse({"detail": "Authentication failed"}, status=401)

        return JsonResponse({"message": f"Auth test successful for user {user_id}"})


@method_decorator(csrf_exempt, name="dispatch")
class UserView(View):
    def post(self, request):
        """Create a new user"""
        try:
            data = json.loads(request.body)
            user_id = data.get("id")

            if not user_id:
                return JsonResponse({"detail": "id is required"}, status=400)

            # Create user using the repository
            user = crud.create_user(user_id)

            if not user:
                return JsonResponse(
                    {"detail": "user already exists or invalid UUID format"}, status=400
                )

            # Return created user
            return JsonResponse(crud.serialize_user(user), status=201)

        except json.JSONDecodeError:
            return JsonResponse({"detail": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"detail": str(e)}, status=400)

    def delete(self, request):
        """Delete a user"""
        try:
            user_id = request.GET.get("id")
            if not user_id:
                return JsonResponse({"detail": "id parameter is required"}, status=400)

            # Delete user using the repository
            success = crud.delete_user(user_id)

            if success:
                return JsonResponse({"message": "user deleted"}, status=200)
            else:
                return JsonResponse(
                    {"detail": "user not found or invalid UUID format"}, status=404
                )

        except Exception as e:
            return JsonResponse({"detail": str(e)}, status=400)
