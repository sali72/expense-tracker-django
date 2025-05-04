import jwt
from django.conf import settings
from uuid import UUID
import datetime
from typing import Dict, Optional, Tuple
from django.http import JsonResponse
from functools import wraps


def generate_jwt_token(user_id: UUID) -> str:
    """
    Generate a JWT token for the given user ID
    Returns the token as a string
    """
    payload = {
        'sub': str(user_id),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
        'iat': datetime.datetime.utcnow(),
    }
    
    token = jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    
    return token


def validate_token(token: str) -> Tuple[bool, Optional[Dict], Optional[str]]:
    """
    Validate a JWT token
    Returns a tuple of (is_valid, payload, error_message)
    """
    try:
        payload = jwt.decode(
            token, 
            settings.JWT_SECRET_KEY, 
            algorithms=[settings.JWT_ALGORITHM]
        )
        return True, payload, None
    except jwt.ExpiredSignatureError:
        return False, None, "Token has expired"
    except (jwt.InvalidTokenError, jwt.DecodeError):
        return False, None, "Invalid token"


def get_user_id_from_request(request):
    """
    Extract user ID from request's Authorization header
    Returns UUID if successful, None if authentication fails
    """
    auth_header = request.META.get('HTTP_AUTHORIZATION')
    if not auth_header:
        return None

    try:
        # Split header into "Bearer" and token parts
        prefix, token = auth_header.split(' ', 1)
        if prefix.lower() != 'bearer':
            return None
        
        # Validate the token
        is_valid, payload, _ = validate_token(token)
        if not is_valid or 'sub' not in payload:
            return None
            
        # Extract and return the user ID
        return UUID(payload['sub'])
    except (ValueError, TypeError) as e:
        print("Error processing token: ", type(e))
        return None


def jwt_auth_required(view_func):
    """
    Decorator to require JWT authentication for a view.
    If authentication fails, returns a 401 Unauthorized response.
    """
    @wraps(view_func)
    async def wrapper(request, *args, **kwargs):
        user_id = get_user_id_from_request(request)
        if not user_id:
            return JsonResponse({"detail": "Authentication required"}, status=401)
        
        # Add user_id to request
        request.user_id = user_id
        
        # Call the view
        return await view_func(request, *args, **kwargs)
    
    return wrapper


class JWTAuthMiddleware:
    """
    Middleware for JWT authentication.
    This middleware checks for JWT tokens in the Authorization header and
    authenticates the user if the token is valid.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Public paths that don't require authentication
        public_paths = [
            '/api/users/login/', 
            '/admin/',
            '/api/users/'  # Registration endpoint (POST only)
        ]
        
        # Paths that require authentication but handled separately
        auth_required_paths = [
            '/api/users/refresh-token/',
        ]
        
        # Skip JWT validation for public paths
        if any(request.path.startswith(path) for path in public_paths):
            # Allow registration but only for POST
            if request.path == '/api/users/' and request.method != 'POST':
                user_id = get_user_id_from_request(request)
                if not user_id:
                    return JsonResponse({"detail": "Authentication required"}, status=401)
            
            # For public paths or POST to users, continue with the request
            return self.get_response(request)
            
        # For paths that have specific auth handling, let the view handle it
        if any(request.path.startswith(path) for path in auth_required_paths):
            # The view will handle authentication using the jwt_auth_required decorator
            return self.get_response(request)
            
        # For all other paths, require authentication
        user_id = get_user_id_from_request(request)
        if not user_id:
            return JsonResponse({"detail": "Authentication required"}, status=401)
            
        # User is authenticated, set user_id in request
        request.user_id = user_id
        
        # Continue with the request
        return self.get_response(request) 