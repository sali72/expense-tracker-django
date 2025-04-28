from datetime import datetime, timedelta
import jwt
from django.conf import settings


def generate_test_access_token(user_id):
    """Generate a JWT token for testing purposes"""
    payload = {"exp": datetime.now() + timedelta(days=30), "sub": str(user_id)}
    return jwt.encode(
        payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )
