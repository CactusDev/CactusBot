"""Manage commands."""

from . import Command


class Meta(Command):
    """Manage commands."""

    COMMAND = "command"

    ROLES = {
        '+': 50,
        '$': 20
    }

    @Command.subcommand
    async def add(self, command: r'!?([+$]?)(.+)', *response, raw: "packet"):
        """Add a command."""

        symbol, name = command

        user_level = self.ROLES.get(symbol, 0)

        raw.role = ''  # HACK
        response = await self.api.add_command(
            name, raw.split(maximum=3)[-1].json, user_level=user_level)
        data = await response.json()

        if data["meta"].get("updated"):
            return "Updated command !{}.".format(name)
        elif data["meta"].get("created"):
            return "Added command !{}.".format(name)

    @Command.subcommand
    async def remove(self, name: "?command"):
        """Remove a command."""
        response = await self.api.remove_command(name)
        if response.status == 200:
            return "Removed command !{}.".format(name)
        return "Command !{} does not exist!".format(name)

    @Command.subcommand
    async def list(self):
        """List all custom commands."""
        response = await self.api.get_command()

        if response.status == 200:
            commands = await response.json()
            return "Commands: {}".format(', '.join(
                command["data"]["attributes"]["name"] for
                command in commands
            ))
        return "No commands added!"
