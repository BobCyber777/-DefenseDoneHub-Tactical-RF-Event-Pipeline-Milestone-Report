import logging

logger = logging.getLogger(__name__)


class ToolRegistry:
    """
    Keeps track of all available Kali tools and avoids duplicate registration.
    """

    def __init__(self):
        self._tools = {}

    def register(self, tool):
        """
        Register a tool instance.
        Each tool must have a unique `name`.
        """
        if not hasattr(tool, "name"):
            raise ValueError("Tool must define a 'name' attribute")

        if tool.name in self._tools:
            logger.warning(f"Tool already registered: {tool.name}")
            return

        self._tools[tool.name] = tool
        logger.info(f"Tool registered: {tool.name}")

    def get(self, name):
        """
        Retrieve a tool by name.
        """
        return self._tools.get(name)

    def all(self):
        """
        Return all registered tools.
        """
        return list(self._tools.values())

    def remove(self, name):
        """
        Remove a tool from registry.
        """
        if name in self._tools:
            del self._tools[name]
            logger.info(f"Tool removed: {name}")

    def clear(self):
        """
        Remove all tools.
        """
        self._tools.clear()
        logger.info("Tool registry cleared")
