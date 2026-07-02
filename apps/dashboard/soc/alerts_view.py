from django.http import JsonResponse
from modules.alerts.manager import AlertManager

alert_manager = AlertManager()


def list_alerts(request):
    alerts = alert_manager.get_active_alerts()

    return JsonResponse([
        {
            "id": a.id,
            "title": a.title,
            "severity": a.severity,
            "status": a.status,
            "score": a.score,
        }
        for a in alerts
    ], safe=False)


def acknowledge_alert(request, alert_id):
    alert_manager.acknowledge(alert_id)
    return JsonResponse({"status": "acknowledged"})


def resolve_alert(request, alert_id):
    alert_manager.resolve(alert_id)
    return JsonResponse({"status": "resolved"})
