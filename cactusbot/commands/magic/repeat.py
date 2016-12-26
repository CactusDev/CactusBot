"""Manage repeats."""

from . import Command

@Command.command()
class Repeat(Command):
    """Manage repeats."""

    COMMAND = "repeat"

    @Command.command()
    async def add(self, *args: False):
        """Add a repeat."""

    @Command.command()
    async def remove(self, repeat_id: r'[1-9]\d*'=None):
        """Remove a repeat"""

    @Command.command(name="list")
    async def list_repeats(self):
        """List all repeats."""
