"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import asyncio

import atexit
import os

from django.core.asgi import get_asgi_application

from config.db import close_motor_client, initialize_beanie

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# Get the ASGI application
application = get_asgi_application()


# Initialize Beanie on startup
async def startup():
    await initialize_beanie()


# Close the Motor client on shutdown
async def shutdown():
    close_motor_client()


# Create an event loop and run the startup function
loop = asyncio.get_event_loop()
loop.run_until_complete(startup())

# Register shutdown handler
atexit.register(lambda: loop.run_until_complete(shutdown()))
