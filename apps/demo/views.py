import random
from django.http import JsonResponse
from django.shortcuts import render

# 1. This renders the main HTML page
def demo_window(request):
    context = {
        "active_alerts": 128,
        "online_sensors": 47,
        "threats_blocked": 15,
        "system_status": "ONLINE"
    }
    return render(request, "demo/demo.html", context)


# 2. This serves the JSON data that your JavaScript fetch() requests every 3 seconds
def demo_api(request):
    return JsonResponse({
        "status": "LIVE DEMO MODE",
        "events": [
            {
                "type": "WIRELESS_BEACON",
                "severity": random.choice(["LOW", "MEDIUM"]),
                "source": "SIM_SENSOR"
            },
            {
                "type": "SOC_CORRELATION",
                "severity": "HIGH" if random.random() > 0.5 else "MEDIUM", # Adding some dynamism
                "source": "ENGINE"
            }
        ]
    })


