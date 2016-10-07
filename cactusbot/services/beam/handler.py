"""Handle data from Beam."""

from logging import getLogger

import json
import asyncio

from ...handler import Handler

from .api import BeamAPI
from .chat import BeamChat
from .constellation import BeamConstellation
from .parser import BeamParser


class BeamHandler:
    """Handle data from Beam services."""

    def __init__(self, channel, handlers):

        self.logger = getLogger(__name__)

        self.api = BeamAPI()
        self.parser = BeamParser()
        self.handlers = handlers  # HACK, potentially

        self._channel = channel
        self.channel = ""

        self.chat = None
        self.constellation = None

        self.chat_events = {
            "ChatMessage": "message"            
        }

    async def run(self, *auth):
        """Connect to Beam chat and handle incoming packets."""
        channel = await self.api.get_channel(self._channel)
        self.channel = str(channel["id"])
        self.api.channel = self.channel  # HACK

        user = await self.api.login(*auth)
        chat = await self.api.get_chat(channel["id"])

        self.chat = BeamChat(channel["id"], *chat["endpoints"])
        await self.chat.connect(user["id"], chat["authkey"])
        asyncio.ensure_future(self.chat.read(self.handle_chat))

    async def handle_chat(self, packet):
        """Handle chat packets."""

        data = packet.get("data")
        if data is None:
            return

        event = packet.get("event")
        if event in self.chat_events:
            event = self.chat_events[event]

            # HACK
            if getattr(self.parser, "parse_" + event):
                data = self.parser.parse_message(data)

            for response in self.handlers.handle(event, data):
                await self.send(response.text)  # HACK

        elif packet.get("id") == "auth":
            if data.get("authenticated") is True:
                await self.send("CactusBot activated. Enjoy! :cactus")
            else:
                self.logger.error("Chat authentication failure!")

    async def send(self, *args, **kwargs):
        """Send a packet to Beam."""

        if self.chat is None:
            raise ConnectionError("Chat not initialized.")

        await self.chat.send(*args, **kwargs)
