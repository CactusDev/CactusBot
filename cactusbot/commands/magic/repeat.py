"""Manage repeats."""

from . import Command


class Repeat(Command):
    """Manage repeats."""

    COMMAND = "repeat"

    @Command.command(role="moderator")
    async def add(self, period: r"[1-9]\d*", command: "?command"):
        """Add a repeat."""

        response = await self.api.add_repeat(command, int(period))

        if response.status == 201:
            return "Repeat !{command} added on interval {period}.".format(
                command=command, period=period)
        elif response.status == 200:
            return "Repeat !{command} updated with interval {period}".format(
                command=command, period=period
            )
        elif response.status == 409:
            return "Repeat already exists!"
        else:
            return "An error occured."

    @Command.command(role="moderator")
    async def remove(self, repeat: "?command"):
        """Remove a repeat"""

        response = await self.api.remove_repeat(repeat)

        if response.status == 200:
            return "Repeat removed."
        elif response.status == 404:
            return "Repeat with ID {} doesn't exist.".format(repeat)

    @Command.command("list", role="moderator")
    async def list_repeats(self):
        """List all repeats."""

        response = await self.api.get_repeats()
        data = (await response.json())["data"]

        if not data:
            return "There are no active repeats in this channel."

        return "Active repeats: {}.".format(', '.join(
            repeat["attributes"]["commandName"] + " {}".format(
                repeat["attributes"]["period"]) for repeat in data))
