"""
DefenseDoneHub Rule Engine Subscriber

Connects:
EventBus → RuleEngine → AlertManager
"""

import logging

from .engine import RuleEngine
from .wireless import OpenWirelessBeaconRule
from modules.alerts.manager import AlertManager

logger = logging.getLogger(__name__)


class RuleSubscriber:
    """
    Bridge between EventBus and Rule Engine.
    """

    def __init__(self):

        self.engine = RuleEngine()
        self.alert_manager = AlertManager()

        # Register rules
        self.engine.register(OpenWirelessBeaconRule())

    async def handle(self, event):

        # Step 1: Run rules
        rule_results = await self.engine.evaluate(event)

        if not rule_results:
            return

        # Step 2: Convert RuleResults → Alerts
        alerts = self.alert_manager.process(rule_results)

        # Step 3: Log outcome (temporary visibility layer)
        for alert in alerts:

            logger.info(
                "[INCIDENT] %s | %s | score=%s | status=%s",
                alert.title,
                alert.severity,
                alert.score,
                alert.status,
            )



