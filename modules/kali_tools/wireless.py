import asyncio
import logging
from .base import KaliTool

logger = logging.getLogger(__name__)


class WirelessMonitorTool(KaliTool):
    """
    RF/Wi-Fi monitoring abstraction layer.

    This does NOT directly depend on Kali tools yet.
    It defines a clean interface for:
    - monitor mode control
    - frame ingestion pipeline
    - normalization into SecurityEvent-compatible output
    """

    name = "wireless_monitor"

    def __init__(self, interface="wlan0mon"):
        super().__init__()
        self.interface = interface
        self.queue = asyncio.Queue()

    async def start(self):
        """
        Start wireless monitoring layer.
        (Later we plug in airodump/kismet/tcpdump here)
        """
        self.running = True
        logger.info(f"[Wireless] Starting monitor on {self.interface}")

        # Placeholder: simulate RF frames for now
        asyncio.create_task(self._simulate_frames())

    async def stop(self):
        self.running = False
        logger.info(f"[Wireless] Stopping monitor on {self.interface}")

    async def collect(self):
        """
        Pull normalized RF events from internal queue.
        """
        events = []

        while not self.queue.empty():
            events.append(await self.queue.get())

        return events

    async def _simulate_frames(self):
        """
        TEMPORARY: simulates RF events until real tools are attached.
        Replace later with:
            - airodump-ng parser
            - kismet JSON stream
            - pyshark/tcpdump ingestion
        """

        counter = 0

        while self.running:
            await asyncio.sleep(2)

            counter += 1

            event = {
                "event_type": "OPEN_WIRELESS_BEACON",
                "severity": "MEDIUM",
                "description": f"Simulated RF frame stream {counter}",
                "rssi": -42,
                "source": self.interface,
            }

            await self.queue.put(event)

            logger.info("[Wireless] Generated RF event")
