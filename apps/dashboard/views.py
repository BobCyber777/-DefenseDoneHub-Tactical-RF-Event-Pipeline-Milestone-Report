from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .models import SecurityEvent


def index(request):
    """
    Landing page for DefenseDoneHub.
    """
    return render(request, "dashboard/index.html")


def soc_dashboard(request):
    """
    Display active SOC alerts awaiting analyst triage.
    """
    logs = SecurityEvent.objects.filter(is_triaged=False)

    severity_filter = request.GET.get("severity")
    if severity_filter in ["LOW", "MEDIUM", "HIGH"]:
        logs = logs.filter(severity=severity_filter)

    return render(
        request,
        "dashboard/soc_triage.html",
        {"logs": logs},
    )


@require_POST
def close_incident(request, pk):
    """
    Mark an incident as triaged.
    """
    event = get_object_or_404(SecurityEvent, pk=pk)
    event.is_triaged = True
    event.save()

    return JsonResponse({
        "status": "success",
        "message": f"Incident {pk} triaged and closed."
    })




