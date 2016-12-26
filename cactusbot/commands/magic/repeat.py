"""Manage repeats."""

from . import Command

@Command.command()
class Repeat(Command):
    """Manage repeats."""

    COMMAND = "repeat"

    @Command.command()
    async def add(self, period: r"[1-9]\d*", command: r"!?\w{1,32}", *args: False):
        """Add a repeat."""

        response = await self.api.add_repeat(command, period, *args)
        print(response.status)

        if response.status == 201:
            return "Repeat !{command} added on interval {period}!".format(
                command=command, period=period)
        else:
            print("UH OH")
            print(await response.json())

    @Command.command()
    async def remove(self, repeat: r'[1-9]\d*'=None):
        """Remove a repeat"""

        response = await self.api.remove_repeat(repeat)

        if response.status == 200:
            return "Repeat removed!"

    @Command.command(name="list")
    async def list_repeats(self):
        """List all repeats."""

        response = await self.api.get_repeats()
        data = (await response.json())["data"]

        return "Active repeats in this channel: {}".format(
            repeat["attributes"]["commandName"] for repeat in data)
