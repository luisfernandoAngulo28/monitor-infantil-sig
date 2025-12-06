"""
ASGI config for Monitor Infantil SIG project.

Expone la aplicación ASGI como una variable a nivel de módulo llamada ``application``.

Para más información sobre este archivo, ver:
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""
import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Inicializar Django ASGI application primero
django_asgi_app = get_asgi_application()

# Importar routing después de inicializar Django
from apps.gis_tracking.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    # HTTP tradicional (Django views)
    "http": django_asgi_app,
    
    # WebSocket handler para GPS tracking en tiempo real
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                websocket_urlpatterns
            )
        )
    ),
})
