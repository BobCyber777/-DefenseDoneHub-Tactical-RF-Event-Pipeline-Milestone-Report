print("Demo websocket routing loaded")

from django.urls import re_path
from .consumers.dashboard import DashboardConsumer

websocket_urlpatterns = [
    re_path(r"^ws/dashboard/$", DashboardConsumer.as_asgi()),
]


