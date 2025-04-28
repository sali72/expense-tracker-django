import pytest
import requests
import uuid
import jwt
from django.conf import settings


def generate_and_validate_token():
    """
    Test that we can generate a token and validate it locally using our auth module.
    """
    # This is a simulated integration test since we're not actually calling an external auth service
    # Create a payload similar to what an auth service would generate
    user_id = str(uuid.uuid4())
    payload = {"sub": user_id}
    
    # Generate a token
    token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    
    # Now decode it to validate
    decoded = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    
    # Verify the decoded payload matches what we expect
    assert decoded["sub"] == user_id
    
    return token 