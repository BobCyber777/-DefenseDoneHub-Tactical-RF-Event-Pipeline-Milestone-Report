from django.contrib import admin
from django.urls import path, include
from apps.dashboard import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='dashboard_index'),
    path('demo/', include('apps.demo.urls')),
]
