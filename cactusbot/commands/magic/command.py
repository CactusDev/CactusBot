"""Manage commands."""


from . import Command
from ...packets import MessagePacket


class Meta(Command):
    """Manage commands."""

    COMMAND = "command"

    permissions = {
        '+': "Mod",
        '$': "Subscriber"
    }

    @Command.subcommand
    async def add(self, name: r'!?([+$]?)(.+)', *response,
                  added_by: "username"):
        """Add a command."""

        permissions = ','.join(self.permissions[symbol] for symbol in name[0])

        data = await self.api.add_command(
            name[1], ' '.join(response), permissions=permissions,
            added_by=added_by
        )
        if data[0].get("meta")["updated"]:
            return MessagePacket("Updated command !{}.".format(name[1]))
        elif data[0].get("meta")["created"]:
            return MessagePacket("Added command !{}.".format(name[1]))

    @Command.subcommand
    async def remove(self, name: "?command", *, removed_by: "username"):
        """Remove a command."""
        removed = await self.api.remove_command(name, removed_by=removed_by)
        if removed:
            return MessagePacket("Removed command !{}.".format(name))
        return MessagePacket("Command !{} does not exist!".format(name))

    @Command.subcommand
    async def list(self):
        """List all custom commands."""
        commands = await self.api.get_command()

        if commands:
            return MessagePacket("Commands: {}".format(', '.join(
                command["data"]["attributes"]["name"] for
                command in commands
            )))
        return MessagePacket("No commands added!")
