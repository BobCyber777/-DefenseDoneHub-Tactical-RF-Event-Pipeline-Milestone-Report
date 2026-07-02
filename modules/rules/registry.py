"""
DefenseDoneHub Rule Engine

Rule Registry

Responsible for registering and organizing
all available rules.
"""

import logging

logger = logging.getLogger(__name__)


class RuleRegistry:
    """
    Stores every registered rule.
    """

    def __init__(self):
        self._rules = []

    def register(self, rule):
        """
        Register a rule instance.
        """

        if not getattr(rule, "enabled", True):
            logger.info(
                "[Rules] Skipping disabled rule: %s",
                rule.name,
            )
            return

        self._rules.append(rule)

        # Lower priority executes first
        self._rules.sort(key=lambda r: r.priority)

        logger.info(
            "[Rules] Registered: %s (priority=%s)",
            rule.name,
            rule.priority,
        )

    def unregister(self, name):
        """
        Remove a rule by name.
        """

        before = len(self._rules)

        self._rules = [
            r for r in self._rules
            if r.name != name
        ]

        removed = before - len(self._rules)

        if removed:
            logger.info("[Rules] Unregistered: %s", name)

    def get_rules(self):
        """
        Return rules in execution order.
        """

        return list(self._rules)

    def clear(self):
        """
        Remove every registered rule.
        """

        self._rules.clear()

    def __len__(self):
        return len(self._rules)

    def __iter__(self):
        return iter(self._rules)

    def __repr__(self):
        return (
            f"<RuleRegistry rules={len(self._rules)}>"
        )
