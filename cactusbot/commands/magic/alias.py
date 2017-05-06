"""Alias command."""

from . import Command
from ...packets import MessagePacket


class Alias(Command):
    """Alias command."""

    COMMAND = "alias"
    ROLE = "moderator"

    @Command.command()
    async def add(self, alias: "?command", command: "?command", *_: False,
                  raw: "packet"):
        """Add a new command alias."""

        _, _, _, _, *args = raw.split()

        if args:
            packet_args = MessagePacket.join(
                *args, separator=' ').json["message"]
        else:
            packet_args = None

        response = await self.api.alias.add(command, alias, packet_args)

        if response.status == 201:
            return "Alias !{} for !{} created.".format(alias, command)
        elif response.status == 200:
            return "Alias !{} for !{} updated.".format(alias, command)
        elif response.status == 404:
            return "Command !{} does not exist.".format(command)

    @Command.command()
    async def remove(self, alias: "?command"):
        """Remove a command alias."""

        response = await self.api.alias.remove(alias)
        if response.status == 200:
            return "Alias !{} removed.".format(alias)
        elif response.status == 404:
            return "Alias !{} doesn't exist!".format(alias)

    @Command.command(name="list")
    async def list_aliases(self):
        """List all aliases."""
        response = await self.api.command.get()

        if response.status == 200:
            commands = (await response.json())["data"]
            aliases = [cmd for cmd in commands if cmd.get("type") == "alias"]
            response = "Aliases: {}".format(', '.join(sorted(
                "{} ({})".format(
                    command["attributes"]["name"],
                    command["attributes"]["commandName"])
                for command in aliases
            )))
            if aliases:
                return response
        return "No aliases added!"
