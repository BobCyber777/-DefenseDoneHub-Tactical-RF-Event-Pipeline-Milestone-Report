from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.index, name="index"),
    path("soc/", views.soc_dashboard, name="soc_dashboard"),
    path("incident/<int:pk>/close/", views.close_incident, name="close_incident"),
    path("widgets/threat-level/", views.widget_threat_level, name="widget_threat_level"),
]



