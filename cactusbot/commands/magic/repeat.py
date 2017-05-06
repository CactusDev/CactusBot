"""Manage repeats."""

from . import Command


class Repeat(Command):
    """Manage repeats."""

    COMMAND = "repeat"
    ROLE = "moderator"

    @Command.command()
    async def add(self, period: r"[1-9]\d*", command: "?command"):
        """Add a repeat."""

        response = await self.api.repeat.add(command, int(period))

        if response.status == 201:
            return "Repeat !{command} added on interval {period}.".format(
                command=command, period=period)
        elif response.status == 200:
            return "Repeat !{command} updated with interval {period}".format(
                command=command, period=period
            )
        elif response.status == 400:
            json = await response.json()
            if json["errors"].get("period", []):
                return json["errors"]["period"][0]
        else:
            return "An error occured."

    @Command.command()
    async def remove(self, repeat: "?command"):
        """Remove a repeat"""

        response = await self.api.repeat.remove(repeat)

        if response.status == 200:
            return "Repeat removed."
        elif response.status == 404:
            return "Repeat with ID {} doesn't exist.".format(repeat)

    @Command.command(name="list")
    async def list_repeats(self):
        """List all repeats."""

        response = await self.api.repeat.get()
        data = (await response.json())["data"]

        if not data:
            return "There are no active repeats in this channel."

        return "Active repeats: {}.".format(', '.join(
            repeat["attributes"]["commandName"] + " {}".format(
                repeat["attributes"]["period"]) for repeat in data))
