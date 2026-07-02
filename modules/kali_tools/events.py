from dataclasses import dataclass
from datetime import datetime


@dataclass
class KaliEvent:
    event_type: str
    severity: str
    description: str
    rssi: int = None
    source: str = "kali"
    created_at: datetime = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()
