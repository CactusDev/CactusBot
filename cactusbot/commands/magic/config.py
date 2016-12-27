"""Config command."""

from .command import Command


@Command.command()
class Config(Command):
    """Config command"""

    COMMAND = "config"

    @Command.command()
    async def announce(self, *args: False):
        """Announce subcommand."""

        if not args:
            return "You must supply an attribute!"

        print(args)

        if args[0].lower() not in ["follow", "subscribe", "host"]:
            return "Invalid announcement type. Available: follow, subscribe, host"
        else:
            if len(args) == 1:
                return "You must specify a message for the announcement!"
            message = ' '.join(args)

            response = await self.api.update_config({"announce": {args[0]: {"message": message}}})
            if response.status == 200:
                return "Updated announcment"
