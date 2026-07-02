from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class SecurityEvent:
    event_type: str
    severity: str
    description: str = ""
    rssi: Optional[int] = None
    source: str = "main"
    timestamp: datetime = datetime.utcnow()
