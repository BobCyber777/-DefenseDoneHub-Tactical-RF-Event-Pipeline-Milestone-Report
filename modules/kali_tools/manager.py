import asyncio
import logging

logger = logging.getLogger(__name__)


class KaliToolManager:
    """
    Central orchestrator for all Kali tool modules.
    Starts, stops, and collects events from registered tools.
    """

    def __init__(self, event_bus=None):
        self.tools = []
        self.event_bus = event_bus
        self.running = False

    def register(self, tool):
        """
        Register a tool that inherits from KaliTool.
        """
        self.tools.append(tool)
        logger.info(f"Registered tool: {tool.name}")

    async def start_all(self):
        """
        Start all registered tools concurrently.
        """
        self.running = True
        logger.info("Starting all Kali tools...")

        tasks = []
        for tool in self.tools:
            tasks.append(asyncio.create_task(tool.start()))

        await asyncio.gather(*tasks)
        logger.info("All tools started.")

    async def stop_all(self):
        """
        Stop all registered tools.
        """
        self.running = False
        logger.info("Stopping all Kali tools...")

        tasks = []
        for tool in self.tools:
            tasks.append(asyncio.create_task(tool.stop()))

        await asyncio.gather(*tasks)
        logger.info("All tools stopped.")

    async def collect_loop(self, interval=0.5):
        """
        Continuous event collection loop.
        Pushes everything into EventBus if available.
        """
        logger.info("Starting tool collection loop...")

        while self.running:
            for tool in self.tools:
                try:
                    events = await tool.collect()

                    if not events:
                        continue

                    for event in events:
                        if self.event_bus:
                            self.event_bus.publish(event)

                except Exception as e:
                    logger.error(f"Tool {tool.name} failed: {e}")

            await asyncio.sleep(interval)
