"""Handles the in-bot, channel-specific currency"""

from . import Command
from ...packets import MessagePacket


class Points(Command):
    """Says stuff and does things"""

    COMMAND = "points"

    @Command.command(hidden=True)
    async def default(self):
        """Get the current user's current # of points"""
        # response = await self.api.points.get()
        # data = (await response.json()["data"])
        # if not data:
        #     return MessagePacket("Splosions!")
        # return MessagePacket(str(data))

        return MessagePacket("lol!")
