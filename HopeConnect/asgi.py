"""
ASGI config for hopeconnect project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os, django
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from orphanages.routing import websocket_urlpatterns   # new

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hopeconnect.settings")
django.setup()

application = ProtocolTypeRouter({
    "http":  get_asgi_application(),
    "websocket": URLRouter(websocket_urlpatterns),
})
