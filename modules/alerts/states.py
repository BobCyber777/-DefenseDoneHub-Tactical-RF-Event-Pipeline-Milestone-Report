"""
DefenseDoneHub Alert System

Alert lifecycle states.
"""

from enum import Enum


class AlertStatus(str, Enum):
    """
    Lifecycle state of an alert.
    """

    ACTIVE = "active"
    ACKNOWLEDGED = "acknowledged"
    INVESTIGATING = "investigating"
    RESOLVED = "resolved"
    ARCHIVED = "archived"
    SUPPRESSED = "suppressed"


class AlertSeverity(str, Enum):
    """
    Severity levels for alerts.
    """

    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
