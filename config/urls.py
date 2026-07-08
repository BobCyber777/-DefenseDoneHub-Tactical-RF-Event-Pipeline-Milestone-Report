from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", include("apps.dashboard.urls")),
    path("demo/", include("apps.demo.urls")),
    path("occ/", include("modules.occ.urls")),
]


