"""
Correlation Engine

Entity model (device / threat representation)
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, List


@dataclass
class Entity:

    entity_id: str

    first_seen: datetime = field(default_factory=datetime.utcnow)
    last_seen: datetime = field(default_factory=datetime.utcnow)

    event_count: int = 0

    sources: List[str] = field(default_factory=list)

    fingerprints: List[str] = field(default_factory=list)

    metadata: Dict[str, Any] = field(default_factory=dict)

    def update(self, event, fingerprint: str):

        self.last_seen = datetime.utcnow()
        self.event_count += 1

        if event.source not in self.sources:
            self.sources.append(event.source)

        if fingerprint not in self.fingerprints:
            self.fingerprints.append(fingerprint)
