from abc import ABC, abstractmethod


class KaliTool(ABC):
    """
    Base interface for every Kali Linux tool integrated into DefenseDoneHub.
    """

    name = "unknown"

    def __init__(self):
        self.running = False

    @abstractmethod
    async def start(self):
        """
        Start the tool.
        """
        pass

    @abstractmethod
    async def stop(self):
        """
        Stop the tool cleanly.
        """
        pass

    @abstractmethod
    async def collect(self):
        """
        Return parsed events from the tool.
        """
        pass

    def status(self):
        return {
            "tool": self.name,
            "running": self.running,
        }
