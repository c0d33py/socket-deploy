"""
ASGI config for server project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from django.urls import path

from tracker.consumers import TaskUpdateConsumerV2

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        # Just HTTP for now. (We can add other protocols later.)
        'websocket': AllowedHostsOriginValidator(
            AuthMiddlewareStack(
                URLRouter(
                    [
                        path("ws/task_update/", TaskUpdateConsumerV2.as_asgi()),
                    ]
                )
            ),
        ),
    }
)
