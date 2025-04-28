import json
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import UserProfile
from .auth import get_user_id_from_request
from uuid import UUID


@method_decorator(csrf_exempt, name='dispatch')
class TestAuthView(View):
    def get(self, request):
        """Test authentication endpoint"""
        user_id = get_user_id_from_request(request)
        if not user_id:
            return JsonResponse({"detail": "Authentication failed"}, status=401)
            
        return JsonResponse({"message": f"Auth test successful for user {user_id}"})


@method_decorator(csrf_exempt, name='dispatch')
class UserView(View):
    def post(self, request):
        """Create a new user"""
        try:
            data = json.loads(request.body)
            user_id = data.get('id')
            
            if not user_id:
                return JsonResponse({"detail": "id is required"}, status=400)
                
            try:
                user_id = UUID(user_id)
            except ValueError:
                return JsonResponse({"detail": "Invalid UUID format"}, status=400)
                
            # Check if user already exists
            if UserProfile.objects.filter(id=user_id).exists():
                return JsonResponse({"detail": "user already exists"}, status=400)
                
            # Create user
            user = UserProfile.objects.create(id=user_id)
            
            # Return created user
            return JsonResponse({
                'id': str(user.id),
                'expense_ids': user.expense_ids
            }, status=201)
            
        except json.JSONDecodeError:
            return JsonResponse({"detail": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"detail": str(e)}, status=400)
    
    def delete(self, request):
        """Delete a user"""
        try:
            user_id = request.GET.get('id')
            if not user_id:
                return JsonResponse({"detail": "id parameter is required"}, status=400)
                
            try:
                user_id = UUID(user_id)
            except ValueError:
                return JsonResponse({"detail": "Invalid UUID format"}, status=400)
                
            try:
                user = UserProfile.objects.get(id=user_id)
                user.delete()
                return JsonResponse({"message": "user deleted"}, status=200)
            except UserProfile.DoesNotExist:
                return JsonResponse({"detail": "user not found"}, status=404)
                
        except Exception as e:
            return JsonResponse({"detail": str(e)}, status=400)
