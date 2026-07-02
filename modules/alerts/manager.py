"""
DefenseDoneHub Alert System

Alert Manager:
Converts RuleResults into Alerts
and manages lifecycle operations.
"""

import logging
import hashlib
from datetime import datetime

from .models import Alert
from .states import AlertSeverity, AlertStatus
from .registry import AlertRegistry

logger = logging.getLogger(__name__)


class AlertManager:
    """
    Core orchestration layer for alerts.
    """

    def __init__(self):
        self.registry = AlertRegistry()

    def _build_fingerprint(self, result) -> str:
        """
        Create a deterministic fingerprint
        to group similar alerts.
        """

        base = f"{result.rule}|{getattr(result.event, 'source', '')}|{getattr(result.event, 'event_type', '')}"

        return hashlib.sha256(base.encode()).hexdigest()

    def _map_severity(self, score: int) -> AlertSeverity:
        """
        Convert rule score into alert severity.
        """

        if score >= 85:
            return AlertSeverity.CRITICAL
        if score >= 70:
            return AlertSeverity.HIGH
        if score >= 40:
            return AlertSeverity.MEDIUM
        if score >= 20:
            return AlertSeverity.LOW
        return AlertSeverity.INFO

    def from_rule_result(self, result):
        """
        Convert RuleResult → Alert.
        """

        fingerprint = self._build_fingerprint(result)
        severity = self._map_severity(result.score)

        alert = Alert(
            id=fingerprint[:12],
            title=result.title,
            description=result.message,
            severity=severity,
            status=AlertStatus.ACTIVE,
            score=result.score,
            source_event=result.event,
            rule=result.rule,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            fingerprint=fingerprint,
            metadata=result.metadata,
        )

        return self.registry.add(alert)

    def process(self, rule_results):
        """
        Process multiple RuleResults.
        """

        alerts = []

        for result in rule_results:
            try:
                alert = self.from_rule_result(result)
                alerts.append(alert)

                logger.info(
                    "[ALERT] %s | %s | score=%s",
                    alert.title,
                    alert.severity,
                    alert.score,
                )

            except Exception:
                logger.exception(
                    "[ALERT] Failed to process RuleResult"
                )

        return alerts

    def get_active_alerts(self):
        return self.registry.active()

    def acknowledge(self, fingerprint: str):
        alert = self.registry.get(fingerprint)
        if alert:
            alert.acknowledge()
            logger.info("[ALERT] Acknowledged %s", fingerprint)

    def resolve(self, fingerprint: str):
        alert = self.registry.get(fingerprint)
        if alert:
            alert.resolve()
            logger.info("[ALERT] Resolved %s", fingerprint)

    def archive(self, fingerprint: str):
        alert = self.registry.get(fingerprint)
        if alert:
            alert.archive()
            logger.info("[ALERT] Archived %s", fingerprint)
