"""
DefenseDoneHub Rule Engine

Wireless Detection Rules
"""

from .base import Rule
from .result import RuleResult


class OpenWirelessBeaconRule(Rule):
    """
    Detects unsecured wireless beacon events.
    """

    name = "open_wireless_beacon"

    description = (
        "Detect unsecured wireless beacon transmissions."
    )

    priority = 100

    def matches(self, event):
        """
        Determine whether this rule applies.
        """

        return (
            getattr(event, "event_type", None)
            == "OPEN_WIRELESS_BEACON"
        )

    async def evaluate(self, event, context):
        """
        Evaluate an open wireless beacon event.
        """

        score = 60

        if event.rssi is not None:

            if event.rssi > -45:
                score += 20

            elif event.rssi > -60:
                score += 10

        return RuleResult(
            rule=self.name,
            severity="MEDIUM",
            score=score,
            title="Open Wireless Beacon",
            message=event.description,
            event=event,
            metadata={
                "source": event.source,
                "rssi": event.rssi,
            },
        )
