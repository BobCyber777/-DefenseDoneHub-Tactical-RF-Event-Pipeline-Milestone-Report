from django.contrib import admin
from django.urls import path
from apps.dashboard import views  # Import your dashboard views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='dashboard_index'),  # Maps http://127.0.0.1:8000/
]


