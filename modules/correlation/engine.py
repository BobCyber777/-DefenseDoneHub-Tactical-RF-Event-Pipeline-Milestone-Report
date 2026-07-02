"""
Correlation Engine

Turns events into tracked entities.
"""

from .fingerprints import FingerprintBuilder
from .tracker import EntityTracker


class CorrelationEngine:

    def __init__(self):
        self.tracker = EntityTracker()

    def process(self, event):
        """
        Convert event → entity association
        """

        fingerprint = FingerprintBuilder.from_event(event)

        # Simple heuristic entity ID (we improve later)
        entity_id = f"{event.source}:{event.event_type}"

        entity = self.tracker.get_or_create(
            entity_id,
            event,
            fingerprint,
        )

        return {
            "entity_id": entity.entity_id,
            "event_count": entity.event_count,
            "sources": entity.sources,
            "last_seen": entity.last_seen,
            "fingerprints": len(entity.fingerprints),
        }
