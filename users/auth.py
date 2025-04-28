import jwt
from django.conf import settings
from uuid import UUID


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
        # Decode the token
        payload = jwt.decode(
            token, 
            settings.JWT_SECRET_KEY, 
            algorithms=[settings.JWT_ALGORITHM]
        )
        
        # Extract and return the user ID
        return UUID(payload['sub'])
    except (ValueError, jwt.DecodeError, jwt.ExpiredSignatureError) as e:
        print("Error decoding token: ", type(e))
        return None 