"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
import logging
from django.core.wsgi import get_wsgi_application

logger = logging.getLogger(__name__)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Get the standard Django WSGI application
application = get_wsgi_application()

logger.warning(
    "Running in WSGI mode. Async views and async database operations "
    "may not work correctly. Consider using ASGI (config.asgi:application) "
    "for production deployment with async functionality."
)
