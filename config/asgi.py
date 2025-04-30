
"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
import atexit
import asyncio

from django.core.asgi import get_asgi_application
from config.db import close_motor_client, initialize_beanie

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# Get the Django ASGI application
django_application = get_asgi_application()

# Flag to track if Beanie has been initialized
beanie_initialized = False
initialization_lock = asyncio.Lock()

# Create a wrapper for the ASGI application that initializes Beanie on startup
async def application(scope, receive, send):
    global beanie_initialized
    
    # Handle lifespan protocol
    if scope["type"] == "lifespan":
        message = await receive()
        if message["type"] == "lifespan.startup":
            # Initialize Beanie during startup
            await initialize_beanie()
            beanie_initialized = True
            await send({"type": "lifespan.startup.complete"})
        elif message["type"] == "lifespan.shutdown":
            # Close MongoDB connection during shutdown
            close_motor_client()
            await send({"type": "lifespan.shutdown.complete"})
        return
    
    # Ensure Beanie is initialized for HTTP/WebSocket requests
    if not beanie_initialized:
        # Use a lock to prevent multiple concurrent initializations
        async with initialization_lock:
            if not beanie_initialized:
                await initialize_beanie()
                beanie_initialized = True
    
    # Pass the request to the Django application
    await django_application(scope, receive, send)

# Register shutdown handler
atexit.register(close_motor_client)
