from dataclasses import dataclass, field
from datetime import datetime
from typing import List


@dataclass
class TimelineEvent:
    event: str
    timestamp: datetime = field(default_factory=datetime.utcnow)


class TimelineStore:

    def __init__(self):
        self.store = {}

    def add_event(self, alert_id: str, event: str):
        if alert_id not in self.store:
            self.store[alert_id] = []

        self.store[alert_id].append(
            TimelineEvent(event=event)
        )

    def get_timeline(self, alert_id: str) -> List[TimelineEvent]:
        return self.store.get(alert_id, [])
