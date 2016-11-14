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
    async def add(self, command: r'!?([+$]?)(.+)', *response,
                  added_by: "username"):
        """Add a command."""

        symbol, name = command

        user_level = self.ROLES.get(symbol, 0)

        response = await self.api.add_command(
            name, ' '.join(response), user_level=user_level)
        data = await response.json()

        if data["meta"].get("updated"):
            return "Updated command !{}.".format(name)
        elif data["meta"].get("created"):
            return "Added command !{}.".format(name)

    @Command.subcommand
    async def remove(self, name: "?command", *, removed_by: "username"):
        """Remove a command."""
        removed = await self.api.remove_command(name, removed_by=removed_by)
        if removed:
            return "Removed command !{}.".format(name)
        return "Command !{} does not exist!".format(name)

    @Command.subcommand
    async def list(self):
        """List all custom commands."""
        commands = await self.api.get_command()

        if commands:
            return "Commands: {}".format(', '.join(
                command["data"]["attributes"]["name"] for
                command in commands
            ))
        return "No commands added!"
