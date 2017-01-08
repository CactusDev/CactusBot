"""Manage commands."""

from . import Command


class Meta(Command):
    """Manage commands."""

    COMMAND = "command"

    ROLES = {
        '+': 4,
        '$': 2
    }

    @Command.command(role="moderator")
    async def add(self, command: r'!?([+$]?)([\w-]{1,32})', *response,
                  raw: "packet"):
        """Add a command."""

        symbol, name = command

        user_level = self.ROLES.get(symbol, 1)

        raw.role = user_level  # HACK
        raw.target = None
        response = await self.api.add_command(
            name, raw.split(maximum=3)[-1].json, user_level=user_level)
        data = await response.json()

        if data["meta"].get("created"):
            return "Added command !{}.".format(name)
        return "Updated command !{}.".format(name)

    @Command.command(role="moderator")
    async def remove(self, name: "?command"):
        """Remove a command."""
        response = await self.api.remove_command(name)
        if response.status == 200:
            return "Removed command !{}.".format(name)
        return "Command !{} does not exist!".format(name)

    @Command.command("list", role="moderator")
    async def list_commands(self):
        """List all custom commands."""
        response = await self.api.get_command()

        if response.status == 200:
            commands = (await response.json())["data"]
            return "Commands: {}".format(', '.join(sorted(
                command["attributes"]["name"] for command in commands
                if command.get("type") == "command"
            )))
        return "No commands added!"

    @Command.command(role="moderator")
    async def enable(self, command: "?command"):
        """Enable a command."""

        response = await self.api.toggle_command(command, True)
        if response.status == 200:
            return "Command !{} has been enabled.".format(command)

    @Command.command(role="moderator")
    async def disable(self, command: "?command"):
        """Disable a command."""

        response = await self.api.toggle_command(command, False)
        if response.status == 200:
            return "Command !{} has been disabled.".format(command)

    @Command.command(role="moderator")
    async def count(self, command: r'?command',
                    action: r"([=+-]?)(\d+)"=None):
        """Update the count of a command."""

        if action is None:
            response = await self.api.get_command(command)
            data = await response.json()
            if response.status == 404:
                return "Command !{} does not exist.".format(command)
            elif response.status == 200:
                return "!{command}'s count is {count}.".format(
                    command=command, count=data["data"]["attributes"]["count"])

        operator, value = action
        action_string = (operator or '=') + value

        response = await self.api.update_command_count(command, action_string)
        if response.status == 200:
            return "Count updated."
