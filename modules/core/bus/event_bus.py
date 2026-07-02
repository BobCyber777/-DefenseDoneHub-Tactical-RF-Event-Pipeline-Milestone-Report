import asyncio
import logging

logger = logging.getLogger(__name__)


class EventBus:
    def __init__(self):
        # Using a list, but we ensure uniqueness during subscription
        self.subscribers = []

    def subscribe(self, handler):
        """Registers an event handler if it hasn't been registered already."""
        if handler not in self.subscribers:
            self.subscribers.append(handler)

    async def publish(self, event):
        """Dispatches events to both sync and async subscribers safely."""
        logger.info(f"[{event.severity}] {event.event_type}")

        for handler in self.subscribers:
            try:
                # Check the function type before invocation
                if asyncio.iscoroutinefunction(handler):
                    await handler(event)
                else:
                    handler(event)

            except Exception as e:
                # Safely get the name of the handler for reliable logging
                handler_name = getattr(handler, "__name__", str(handler))
                logger.error(
                    f"Handler '{handler_name}' failed processing event: {e}", 
                    exc_info=True
                )




