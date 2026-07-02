"""
Correlation Engine

Fingerprint generation for entity tracking.
"""

import hashlib


class FingerprintBuilder:

    @staticmethod
    def from_event(event):
        """
        Create deterministic fingerprint from any event.
        """

        base = f"{event.source}|{event.event_type}|{getattr(event, 'rssi', '')}"

        return hashlib.sha256(base.encode()).hexdigest()

    @staticmethod
    def weak_cluster_key(event):
        """
        Looser grouping for correlation (less strict than fingerprint).
        """

        return f"{event.source}:{event.event_type}"
