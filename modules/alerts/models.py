"""
DefenseDoneHub Alert System

Alert data model.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Optional

from .states import AlertStatus, AlertSeverity


@dataclass(slots=True)
class Alert:
    """
    Operator-facing security alert.
    """

    id: str
    title: str
    description: str

    severity: AlertSeverity = AlertSeverity.INFO
    status: AlertStatus = AlertStatus.ACTIVE

    score: int = 0

    source_event: Any = None
    rule: str = ""

    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    # Correlation / grouping key
    fingerprint: Optional[str] = None

    # Extra structured data
    metadata: Dict[str, Any] = field(default_factory=dict)

    def acknowledge(self):
        self.status = AlertStatus.ACKNOWLEDGED
        self.updated_at = datetime.utcnow()

    def resolve(self):
        self.status = AlertStatus.RESOLVED
        self.updated_at = datetime.utcnow()

    def archive(self):
        self.status = AlertStatus.ARCHIVED
        self.updated_at = datetime.utcnow()

    def escalate(self):
        self.updated_at = datetime.utcnow()
        if self.severity == AlertSeverity.LOW:
            self.severity = AlertSeverity.MEDIUM
        elif self.severity == AlertSeverity.MEDIUM:
            self.severity = AlertSeverity.HIGH
        elif self.severity == AlertSeverity.HIGH:
            self.severity = AlertSeverity.CRITICAL
