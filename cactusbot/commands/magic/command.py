"""Manage commands."""


from . import Command


class Meta(Command):
    """Manage commands."""

    __command__ = "command"

    @Command.subcommand
    async def add(self, name: r'!?([+$]?)(.+)', *response,
                  added_by: "username"):
        """Add a command."""
        self.api.add_command(
            name, ' '.join(response),
            added_by=added_by
        )
        return "Added command !{}.".format(name)

    @Command.subcommand
    async def remove(self, name: "?command", *, removed_by: "username"):
        """Remove a command."""
        try:
            self.api.remove_command(name, removed_by=removed_by)
        except Exception:  # TODO
            return "Command !{} does not exist!".format(name)
        else:
            return "Removed command !{}.".format(name)

    @Command.subcommand
    async def list(self):
        """List all custom commands."""
        commands = self.api.get_command()
        if commands:
            return "Commands: {}.".format(
                ', '.join(command["name"] for command in commands)
            )
        return "No commands added."
