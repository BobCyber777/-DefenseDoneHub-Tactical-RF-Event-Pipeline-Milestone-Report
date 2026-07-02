import asyncio

from modules.rules.subscriber import RuleSubscriber
from modules.mission.engine import MissionEngine
from modules.correlation.engine import CorrelationEngine


class Orchestrator:

    def __init__(self, alert_manager):

        self.alert_manager = alert_manager

        self.mission = MissionEngine()
        self.correlation = CorrelationEngine()

        self.running = False

    async def start(self):

        self.running = True

        while self.running:

            await self.tick()

            await asyncio.sleep(1)

    async def tick(self):

        # 1. Get active alerts
        alerts = self.alert_manager.get_active_alerts()

        # 2. Update mission state
        state = self.mission.evaluate(alerts)

        # 3. Correlate alerts into entities
        entities = []

        for alert in alerts:
            entity = self.correlation.process(alert)
            entities.append(entity)

        # 4. Debug output (temporary visibility layer)
        print("\n[ORCHESTRATOR TICK]")
        print("Mission State:", state)
        print("Active Alerts:", len(alerts))
        print("Entities:", len(entities))
