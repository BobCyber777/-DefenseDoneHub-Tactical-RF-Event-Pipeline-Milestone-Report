import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

from apps.dashboard.routing import websocket_urlpatterns as dashboard_ws
from apps.demo.routing import websocket_urlpatterns as demo_ws

django_asgi_app = get_asgi_application()

websocket_urlpatterns = dashboard_ws + demo_ws

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})



