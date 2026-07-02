"""
DefenseDoneHub Rule Engine

Main Rule Engine
"""

import logging

from .context import RuleContext
from .registry import RuleRegistry

logger = logging.getLogger(__name__)


class RuleEngine:
    """
    Executes every registered rule against incoming events.
    """

    def __init__(self):
        self.registry = RuleRegistry()
        self.context = RuleContext()

    def register(self, rule):
        """
        Register a rule.
        """
        self.registry.register(rule)

    async def evaluate(self, event):
        """
        Evaluate a single event.

        Returns:
            list[RuleResult]
        """

        self.context.add_event(event)

        results = []

        logger.debug(
            "[Rules] Evaluating event: %s",
            getattr(event, "event_type", type(event).__name__),
        )

        for rule in self.registry:

            if not rule.enabled:
                continue

            try:

                if not rule.matches(event):
                    continue

                result = await rule.evaluate(
                    event,
                    self.context,
                )

                if result is not None:
                    results.append(result)

                    if hasattr(result, "score"):
                        self.context.increase_score(
                            result.score
                        )

            except Exception:

                logger.exception(
                    "[Rules] %s failed",
                    rule.name,
                )

        return results

    def clear(self):
        """
        Remove all registered rules.
        """
        self.registry.clear()

    @property
    def threat_score(self):
        """
        Current accumulated threat score.
        """
        return self.context.threat_score
