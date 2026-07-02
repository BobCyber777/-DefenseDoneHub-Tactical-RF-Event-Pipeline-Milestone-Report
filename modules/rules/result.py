"""
DefenseDoneHub Rule Engine

Standard result object returned by every rule.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict


@dataclass(slots=True)
class RuleResult:
    """
    Standard output produced by every rule evaluation.
    """

    # Rule metadata
    rule: str
    matched: bool = True

    # Threat assessment
    severity: str = "INFO"
    score: int = 0

    # Human-readable information
    title: str = ""
    message: str = ""

    # Original event
    event: Any = None

    # Additional structured information
    metadata: Dict[str, Any] = field(default_factory=dict)

    # Evaluation timestamp
    timestamp: datetime = field(default_factory=datetime.utcnow)

    @property
    def is_alert(self) -> bool:
        """
        Returns True if this result should be treated as an alert.
        """
        return self.score >= 50

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the result into a serializable dictionary.
        """
        return {
            "rule": self.rule,
            "matched": self.matched,
            "severity": self.severity,
            "score": self.score,
            "title": self.title,
            "message": self.message,
            "metadata": self.metadata,
            "timestamp": self.timestamp.isoformat(),
        }

    def __repr__(self):
        return (
            f"<RuleResult(rule={self.rule}, "
            f"severity={self.severity}, score={self.score})>"
        )
