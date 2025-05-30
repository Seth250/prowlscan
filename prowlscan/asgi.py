"""
ASGI config for prowlscan project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'prowlscan.settings')

# Initialize Django ASGI application early to ensure the AppRegistry is populated before
# importing code that may import ORM models (to avoid an AppRegistryNotReady error)
asgi_application = get_asgi_application()
# another solution is directly calling django.setup() (get_asgi_application calls it)

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

import core.routing


application = ProtocolTypeRouter({
    'http': asgi_application,
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter([
                *core.routing.websocket_urlpatterns,
            ])
        )
    )
})