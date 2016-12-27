"""Manage commands."""

from . import Command


@Command.command()
class Meta(Command):
    """Manage commands."""

    COMMAND = "command"

    ROLES = {
        '+': 50,
        '$': 20
    }

    @Command.command()
    async def add(self, command: r'!?([+$]?)(.+)', *response, raw: "packet"):
        """Add a command."""

        symbol, name = command

        user_level = self.ROLES.get(symbol, 0)

        raw.role = user_level  # HACK
        raw.target = None
        response = await self.api.add_command(
            name, raw.split(maximum=3)[-1].json, user_level=user_level)
        data = await response.json()

        if data["meta"].get("updated"):
            return "Updated command !{}.".format(name)
        elif data["meta"].get("created"):
            return "Added command !{}.".format(name)

    @Command.command()
    async def remove(self, name: "?command"):
        """Remove a command."""
        response = await self.api.remove_command(name)
        if response.status == 200:
            return "Removed command !{}.".format(name)
        return "Command !{} does not exist!".format(name)

    @Command.command(name="list")
    async def list_commands(self):
        """List all custom commands."""
        response = await self.api.get_command()

        if response.status == 200:
            commands = await response.json()
            return "Commands: {}".format(', '.join(
                command["data"]["attributes"]["name"] for
                command in commands
            ))
        return "No commands added!"

    @Command.command()
    async def enable(self, command: r'!?\w{1,32}'):
        """Enable a command."""

        response = await self.api.toggle_command(command, True)
        if response.status == 200:
            return "Command !{} has been enabled.".format(command)

    @Command.command()
    async def disable(self, command: r'!?\w{1,32}'):
        """Disable a command."""

        response = await self.api.toggle_command(command, False)
        if response.status == 200:
            return "Command !{} has been disabled.".format(command)

    @Command.command()
    async def count(self, command: r'!?\w{1,32}', *args: False):
        """Set, add, remove the count of a command."""

        if not args:
            response = await self.api.get_command(command)
            data = await response.json()
            if response.status == 404:
                return "The command !{} doesn't exist!"
            elif response.status == 200:
                return "!{command}'s count is: {count}".format(
                    command=command, count=data["data"]["attributes"]["count"])
