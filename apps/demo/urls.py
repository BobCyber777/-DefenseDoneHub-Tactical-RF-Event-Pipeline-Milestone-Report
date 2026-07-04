from django.urls import path
from .views import demo_window, demo_api

urlpatterns = [
    path('', demo_window),          # public UI window
    path('api/', demo_api),         # single API endpoint
]

