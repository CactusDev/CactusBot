"""Handle data from Beam."""

from logging import getLogger

import json
import asyncio
import time

from ...packets import MessagePacket, EventPacket

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

        self.constellation_events = {
            "channel": {
                "followed": self.on_follow,
                "subscribed": self.on_subscribe,
                "hosted": self.on_host
            }
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

        self.constellation = BeamConstellation(channel["id"], user["id"])
        await self.constellation.connect()
        asyncio.ensure_future(
            self.constellation.read(self.handle_constellation))

    async def handle_chat(self, packet):
        """Handle chat packets."""

        start = int(round(time.time() * 1000))

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
                if callable(response):
                    response = await response(response)
                    print(response)
                await self.send(response.text)  # HACK
                end = int(round(time.time() * 1000))
                print(end - start)

        elif packet.get("id") == "auth":
            if data.get("authenticated") is True:
                await self.send("CactusBot activated. Enjoy! :cactus")
            else:
                self.logger.error("Chat authentication failure!")

    async def handle_constellation(self, packet):
        """Handle constellation packets."""

        packet = json.loads(packet)

        data = packet.get("data")
        if not isinstance(data, dict):
            return

        event = data["channel"].split(":")
        data = data.get("payload")
        if not isinstance(data, dict):
            return

        if event is None:
            return

        if "user" in data:
            if event[0] in self.constellation_events:
                if event[2] in self.constellation_events[event[0]]:
                    data = self.constellation_events[event[0]][event[2]](data)
                    if data is not None:
                        for response in data:
                            await self.send(response.text)

    async def send(self, *args, **kwargs):
        """Send a packet to Beam."""

        if self.chat is None:
            raise ConnectionError("Chat not initialized.")

        await self.chat.send(*args, **kwargs)

    def on_follow(self, data):
        """Handle follow packets from Constellation."""
        if data["following"]:
            return self.handlers.handle("follow", EventPacket("follow", data["user"]["username"]))

    def on_subscribe(self, data):
        """Handle subscribe packets from Constellation."""
        return self.handlers.handle("subscribe", EventPacket("subscribe", data["user"]["username"]))

    def on_host(self, data):
        """Handle host packets from Constellation."""
        return self.handlers.handle("host", EventPacket("host", data["user"]["username"]))
