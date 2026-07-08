import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Callable, Any, Dict, List

# Assuming this import exists in your project structure
# from modules.events.schema import EventEnvelope

logger = logging.getLogger(__name__)


class BaseEventBus(ABC):

    @abstractmethod
    async def publish(self, topic: str, event: Any) -> None:
        """Dispatches events to subscribers of a specific topic."""
        pass

    @abstractmethod
    def subscribe(self, topic: str, handler: Callable) -> None:
        """Registers an event handler to a specific topic."""
        pass


class EventBus(BaseEventBus):
    def __init__(self):
        # Map topics to a list of unique handlers
        self.subscribers: Dict[str, List[Callable]] = {}

    def subscribe(self, topic: str, handler: Callable) -> None:
        """Registers an event handler for a topic if it hasn't been already."""
        if topic not in self.subscribers:
            self.subscribers[topic] = []
        
        if handler not in self.subscribers[topic]:
            self.subscribers[topic].append(handler)

    async def publish(self, topic: str, event: Any) -> None:
        """Dispatches events to both sync and async subscribers safely based on topic."""
        # Safeguard for event attributes if event structure varies
        severity = getattr(event, "severity", "INFO")
        event_type = getattr(event, "event_type", type(event).__name__)
        
        logger.info(f"[{severity}] Publishing to topic '{topic}': {event_type}")

        # If no one is listening to this topic, exit early
        if topic not in self.subscribers:
            return

        for handler in self.subscribers[topic]:
            try:
                # Target the underlying callable if it's an object instance
                callable_target = getattr(handler, "__call__", handler)
                
                if asyncio.iscoroutinefunction(callable_target):
                    await handler(event)
                else:
                    handler(event)

            except Exception as e:
                handler_name = getattr(handler, "__name__", type(handler).__name__)
                logger.error(
                    f"Handler '{handler_name}' failed processing event on topic '{topic}': {e}", 
                    exc_info=True
                )


