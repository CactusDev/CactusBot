"""Handle data from Twitch."""

import asyncio
import logging
from functools import partial

from ...packets import BanPacket, MessagePacket
from .api import TwitchAPI
from .chat import TwitchChat
from .parser import TwitchParser


class TwitchHandler:
    """Handle data from Twitch services."""

    def __init__(self, channel, handlers):

        self.logger = logging.getLogger(__name__)

        self.api = TwitchAPI()
        self.parser = TwitchParser()
        self.handlers = handlers  # HACK, potentially

        self._channel = channel
        self.channel = ""

        self.chat = None

        self.chat_events = {
            "ChatMessage": "message"
        }

    async def run(self, *auth):
        """Connect to Twitch chat and handle incoming packets."""
        channel = await self.api.get_channel(self._channel)
        self.channel = str(channel["id"])
        self.api.channel = self.channel  # HACK

        user = await self.api.login(*auth)
        chat = await self.api.get_chat(channel["id"])

        self.chat = TwitchChat(channel["id"], *chat["endpoints"])
        await self.chat.connect(
            user["id"], partial(self.api.get_chat, channel["id"]))
        asyncio.ensure_future(self.chat.read(self.handle_chat))

        await self.handle("start", None)

    async def handle_chat(self, packet):
        """Handle chat packets."""

        data = packet.get("data")
        if data is None:
            return

        event = packet.get("event")

        if event in self.chat_events:
            event = self.chat_events[event]

            # HACK?
            if getattr(self.parser, "parse_" + event):
                data = getattr(self.parser, "parse_" + event)(data)

            await self.handle(event, data)

    async def handle(self, event, data):
        for response in await self.handlers.handle(event, data):
            if isinstance(response, MessagePacket):
                args, kwargs = self.parser.synthesize(response)
                await self.send(*args, **kwargs)

            elif isinstance(response, BanPacket):
                if response.duration:
                    await self.send(
                        response.user,
                        response.duration,
                        method="timeout"
                    )
                else:
                    pass  # TODO: full ban

    async def send(self, *args, **kwargs):
        """Send a packet to Twitch."""

        if self.chat is None:
            raise ConnectionError("Chat not initialized.")

        await self.chat.send(*args, **kwargs)
