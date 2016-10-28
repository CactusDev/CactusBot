"""Trust command."""

from ..command import Command

class Trust(Command):
    """Trust command."""

    COMMAND = "trust"

    async def get(self, channel: "channel"):
        """Get the trused users in a channel."""
        pass

    async def add(self, *args, channel: "channel"):
        """Add a trusted user."""
        pass

    async def remove(self, *args, channel: "channel"):
        """Remove a trusted user."""
        pass
