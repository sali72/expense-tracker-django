from datetime import datetime, timedelta
import jwt

JWT_SECRET_KEY = "CHANGE THIS IN PRODUCTION"
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_TIME = 30  # days


def generate_test_access_token(user_id):
    """Generate a JWT token for testing purposes"""
    payload = {
        "exp": datetime.now() + timedelta(days=JWT_EXPIRATION_TIME),
        "sub": str(user_id),
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
