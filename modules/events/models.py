from dataclasses import dataclass
from datetime import datetime


@dataclass
class SignalEvent:

    event_type: str
    severity: str
    description: str

    rssi: int | None = None
    source: str | None = None

    timestamp: datetime = datetime.utcnow()
