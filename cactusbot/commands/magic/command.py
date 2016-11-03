"""Manage commands."""


from . import Command


class Meta(Command):
    """Manage commands."""

    COMMAND = "command"

    permissions = {
        '+': "Mod",
        '$': "Subscriber"
    }

    @Command.subcommand
    async def add(self, command: r'!?([+$]?)(.+)', *response,
                  added_by: "username"):
        """Add a command."""

        level, name = command

        permissions = ','.join(self.permissions[symbol] for symbol in level)

        data = await self.api.add_command(
            name, ' '.join(response), permissions=permissions,
            added_by=added_by
        )
        if data[0]["meta"].get("updated"):
            return "Updated command !{}.".format(name)
        elif data[0]["meta"].get("created"):
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
