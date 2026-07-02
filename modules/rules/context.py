"""
DefenseDoneHub Rule Engine

Shared evaluation context.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class RuleContext:
    """
    Shared state passed to every rule evaluation.
    """

    # Current evaluation cycle
    event_count: int = 0

    # Running threat score
    threat_score: int = 0

    # Previous events
    history: List[Any] = field(default_factory=list)

    # Shared data between rules
    metadata: Dict[str, Any] = field(default_factory=dict)

    def add_event(self, event):
        """
        Store an event in the evaluation history.
        """
        self.history.append(event)
        self.event_count += 1

    def set(self, key, value):
        """
        Store shared data.
        """
        self.metadata[key] = value

    def get(self, key, default=None):
        """
        Retrieve shared data.
        """
        return self.metadata.get(key, default)

    def increase_score(self, amount: int):
        """
        Increase the running threat score.
        """
        self.threat_score += amount

    def reset(self):
        """
        Reset the evaluation context.
        """
        self.event_count = 0
        self.threat_score = 0
        self.history.clear()
        self.metadata.clear()
