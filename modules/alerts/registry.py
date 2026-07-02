"""
DefenseDoneHub Alert System

Alert Registry:
- Stores active alerts
- Prevents duplicates
- Tracks lifecycle state in memory
"""

import logging
from typing import Dict, List, Optional

from .models import Alert

logger = logging.getLogger(__name__)


class AlertRegistry:
    """
    In-memory store for active alerts.
    """

    def __init__(self):
        # key: fingerprint -> Alert
        self._alerts: Dict[str, Alert] = {}

    def add(self, alert: Alert) -> Alert:
        """
        Add or update an alert.
        Uses fingerprint to prevent duplicates.
        """

        if alert.fingerprint and alert.fingerprint in self._alerts:
            existing = self._alerts[alert.fingerprint]

            # Update existing alert instead of duplicating
            existing.updated_at = alert.updated_at
            existing.score = max(existing.score, alert.score)
            existing.description = alert.description

            logger.info(
                "[ALERT] Updated existing alert %s",
                alert.fingerprint,
            )

            return existing

        if alert.fingerprint:
            self._alerts[alert.fingerprint] = alert

        logger.info(
            "[ALERT] New alert created: %s",
            alert.title,
        )

        return alert

    def get(self, fingerprint: str) -> Optional[Alert]:
        return self._alerts.get(fingerprint)

    def all(self) -> List[Alert]:
        return list(self._alerts.values())

    def active(self) -> List[Alert]:
        return [
            a for a in self._alerts.values()
            if a.status == "active"
        ]

    def remove(self, fingerprint: str):
        if fingerprint in self._alerts:
            del self._alerts[fingerprint]
            logger.info("[ALERT] Removed %s", fingerprint)

    def clear(self):
        self._alerts.clear()
        logger.info("[ALERT] Registry cleared")

    def __len__(self):
        return len(self._alerts)
