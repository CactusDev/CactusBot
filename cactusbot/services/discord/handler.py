"""Handle data from Beam."""

import logging

import discord

from .parser import DiscordParser
from ...packets import MessagePacket


class DiscordHandler(discord.Client):
    """Handle data from Discord."""

    def __init__(self, handlers):

        super().__init__()

        self.logger = logging.getLogger(__name__)

        self.parser = DiscordParser()
        self.handlers = handlers  # HACK, potentially

    async def on_message(self, message):
        """Handle chat packets."""

        data = self.parser.parse_message(message)

        for response in self.handlers.handle("message", data):
            if isinstance(response, MessagePacket):
                packet = self.parser.synthesize(response)
                await self.send_message(message.channel, packet)

    async def run(self, *args, **kwargs):
        await self.start(*args, **kwargs)
