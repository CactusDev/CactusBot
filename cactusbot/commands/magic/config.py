"""Config command."""

from .command import Command


class Config(Command):
    """Config command"""

    COMMAND = "config"

    @Command.command()
    async def announce(self, attribute, *args):
        """Announce subcommand."""

        if attribute.lower() not in ["announce"]:
            return "Invalid attribute. Available: announce"

        if args[0].lower() not in ["follow", "subscribe", "host"]:
            return "Invalid announcement type. Available: follow, subscribe, host"
        else:
            if not len(args) == 2:
                return "You must specify a message for the announcement!"
