from django.urls import path
from apps.dashboard.consumers import AlertStreamConsumer

websocket_urlpatterns = [
    path('ws/alerts/', AlertStreamConsumer.as_asgi()),
]


