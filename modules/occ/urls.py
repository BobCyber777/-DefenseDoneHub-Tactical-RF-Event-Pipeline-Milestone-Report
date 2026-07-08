from django.urls import path
from . import views

app_name = "occ"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
]
