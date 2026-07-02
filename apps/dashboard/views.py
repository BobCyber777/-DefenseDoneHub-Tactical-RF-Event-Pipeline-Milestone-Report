from django.shortcuts import render
from .models import SecurityEvent


def index(request):

    events = SecurityEvent.objects.order_by("-created_at")[:100]

    return render(
        request,
        "dashboard/index.html",
        {
            "events": events
        }
    )
