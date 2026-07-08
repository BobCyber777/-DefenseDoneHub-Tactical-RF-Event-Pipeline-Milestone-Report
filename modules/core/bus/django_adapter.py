import os
import django
from asgiref.sync import sync_to_async

# 1. Setup Django environment first
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

# 2. Imports that depend on Django setup
from apps.dashboard.models import SecurityEvent
from modules.events.schema import EventEnvelope


@sync_to_async
def django_store_event(event: EventEnvelope):
    """Safely extracts data from the event envelope/payload and saves to Django DB."""
    # Envelope level attributes
    event_type = getattr(event, "event_type", "unknown")
    source = getattr(event, "source", "unknown")
    
    # Safely extract details from the payload dictionary if present
    payload = getattr(event, "payload", {}) if event else {}
    
    SecurityEvent.objects.create(
        event_type=event_type,
        severity=payload.get("severity", "INFO"),  # Extracted from payload
        description=payload.get("description", ""),  # Extracted from payload
        rssi=payload.get("rssi"),  # Extracted from payload
        source=source,
    )


class EventFactory:

    @staticmethod
    def security_alert(payload: dict, correlation_id=None) -> EventEnvelope:
        return EventEnvelope.create(
            event_type="security.alert",
            payload=payload,
            source="django",
            correlation_id=correlation_id,
            metadata={"domain": "soc"},
        )

    @staticmethod
    def sensor_event(payload: dict) -> EventEnvelope:
        return EventEnvelope.create(
            event_type="sensor.telemetry",
            payload=payload,
            source="kali_tools",
            metadata={"stream": "wireless"},
        )



