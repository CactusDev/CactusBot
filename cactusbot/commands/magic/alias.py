"""Alias command."""

from . import Command
from ...packets import MessagePacket


class Alias(Command):
    """Alias command."""

    COMMAND = "alias"

    @Command.command(role="moderator")
    async def add(self, alias: "?command", command: "?command", *_: False,
                  raw: "packet"):
        """Add a new command alias."""

        _, _, _, _, *args = raw.split()

        if args:
            packet_args = MessagePacket.join(
                *args, separator=' ').json["message"]
        else:
            packet_args = None

        response = await self.api.add_alias(command, alias, packet_args)

        if response.status == 201:
            return "Alias !{} for !{} created.".format(alias, command)
        elif response.status == 200:
            return "Alias !{} for command !{} updated.".format(alias, command)
        elif response.status == 404:
            return "Command !{} does not exist.".format(command)

    @Command.command(role="moderator")
    async def remove(self, alias: "?command"):
        """Remove a command alias."""

        response = await self.api.remove_alias(alias)
        if response.status == 200:
            return "Alias !{} removed.".format(alias)
        elif response.status == 404:
            return "Alias !{} doesn't exist!".format(alias)

    @Command.command("list", role="moderator")
    async def list_aliases(self):
        """List all aliases."""
        response = await self.api.get_command()

        if response.status == 200:
            commands = (await response.json())["data"]
            return "Aliases: {}.".format(', '.join(sorted(
                "{} ({})".format(
                    command["attributes"]["name"],
                    command["attributes"]["commandName"])
                for command in commands
                if command.get("type") == "aliases"
            )))
        return "No commands added!"
