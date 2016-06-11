"""Manage commands."""


from .. import Command


class Meta(Command):
    """Manage commands."""

    __command__ = "command"

    @Command.subcommand
    async def add(self, name: r'!?([+$]?)(.+)', *response, user: "username"):
        """Add a command."""
        self.api.add_command(
            name, ' '.join(response),
            addedBy=user
        )
        return "Added command !{}.".format(name)

    @Command.subcommand
    async def remove(self, name: "?command"):
        try:
            self.api.remove_command(name)
        except Exception:  # TODO
            return "Command !{} does not exist!".format(name)
        else:
            return "Removed command !{}.".format(name)

    @Command.subcommand
    async def list(self):
        commands = self.api.get_command()
        if commands:
            return "Commands: {}.".format(
                ', '.join(command["name"] for command in commands)
            )
        return "No commands added."
