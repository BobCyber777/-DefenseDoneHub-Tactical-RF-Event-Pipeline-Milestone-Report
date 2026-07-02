import os
from asgiref.sync import sync_to_async


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django
django.setup()

from apps.dashboard.models import SecurityEvent


@sync_to_async
def django_store_event(event):
    SecurityEvent.objects.create(
        event_type=event.event_type,
        severity=event.severity,
        description=event.description,
        rssi=event.rssi,
        source=event.source,
    )




