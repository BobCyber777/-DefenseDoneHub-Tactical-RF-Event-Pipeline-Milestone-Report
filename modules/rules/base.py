"""
DefenseDoneHub Rule Engine

Base Rule abstraction.

Every detection, correlation, mission,
or policy rule must inherit from Rule.
"""

from abc import ABC, abstractmethod


class Rule(ABC):
    """
    Base class for every DefenseDoneHub rule.
    """

    #: Unique rule identifier
    name = "unnamed_rule"

    #: Human-readable description
    description = ""

    #: Lower executes first
    priority = 100

    #: Enable/disable rule
    enabled = True

    @abstractmethod
    def matches(self, event) -> bool:
        """
        Return True if this rule should evaluate the event.
        """
        raise NotImplementedError

    @abstractmethod
    async def evaluate(self, event, context):
        """
        Evaluate the event.

        Returns:
            RuleResult
            or None
        """
        raise NotImplementedError

    def __repr__(self):
        return f"<Rule {self.name}>"
