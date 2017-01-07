"""Alias command."""

from . import Command


class Alias(Command):
    """Alias command."""

    COMMAND = "alias"

    @Command.command(role="moderator")
    async def add(self, alias: "?command", command: "?command", *args: False,
                  raw: "packet"):
        """Add a new command alias."""

        _, _, _, _, packet_args = raw.split(maximum=4)

        response = await self.api.add_alias(command, alias, packet_args.json)

        if response.status == 201:
            return "Alias {} for command {} created.".format(alias, command)
        elif response.status == 200:
            return "Alias {} for command {} updated.".format(alias, command)

    @Command.command(role="moderator")
    async def remove(self, alias: "?command"):
        """Remove a command alias."""

        response = await self.api.remove_alias(alias)
        if response.status == 200:
            return "Alias {} removed.".format(alias)
        elif response.status == 404:
            return "Alias {} doesn't exist!".format(alias)

    @Command.command("list", role="moderator")
    async def list_aliases(self):
        """List all aliases."""
        response = await self.api.get_command()

        if response.status == 200:
            commands = (await response.json())["data"]
            return "Commands: {}".format(', '.join(sorted(
                "{} ({})".format(
                    command["attributes"]["name"],
                    command["attributes"]["commandName"])
                for command in commands
                if command.get("type") == "aliases"
            )))
        return "No commands added!"
