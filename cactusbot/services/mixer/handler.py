"""Handle data from Mixer."""

import asyncio
import logging
from functools import partial

from ...packets import BanPacket, MessagePacket, Packet
from .api import MixerAPI
from .chat import MixerChat
from .constellation import MixerConstellation
from .parser import MixerParser

CHAT_EVENTS = {
    "ChatMessage": "message",
    "UserJoin": "join",
    "UserLeave": "leave"
}

CONSTELLATION_EVENTS = {
    "channel:followed": "follow",
    "channel:subscribed": "subscribe",
    "channel:resubscribed": "resubscribe",
    "channel:hosted": "host"
}


class MixerHandler:
    """Handle data from Mixer services."""

    def __init__(self, channel, token, handlers):

        self.logger = logging.getLogger(__name__)

        self.api = MixerAPI(channel, token)

        self.parser = MixerParser()
        self.handlers = handlers  # HACK, potentially

        self.channel = channel

        self.chat = None
        self.constellation = None

    async def run(self):
        """Connect to Mixer chat and handle incoming packets."""

        channel = await self.api.get_channel(self.channel)
        self.api.channel = str(channel["id"])

        user_id = channel["userId"]
        chat = await self.api.get_chat(channel["id"])

        bot_channel = await self.api.get_bot_channel()
        bot_id = bot_channel["channel"]["userId"]

        await self.handle("username_update",
                          Packet(username=bot_channel["channel"]["token"]))

        if "authkey" not in chat:
            self.logger.error("Failed to authenticate with Mixer!")

        self.chat = MixerChat(channel["id"], *chat["endpoints"])
        await self.chat.connect(
            bot_id, partial(self.api.get_chat, channel["id"]))
        asyncio.ensure_future(self.chat.read(self.handle_chat))

        self.constellation = MixerConstellation(channel["id"], user_id)
        await self.constellation.connect()
        asyncio.ensure_future(
            self.constellation.read(self.handle_constellation))

        await self.handle("start", None)

    async def handle_chat(self, packet):
        """Handle chat packets."""

        data = packet.get("data")
        if data is None:
            return

        event = packet.get("event")

        if event in CHAT_EVENTS:
            event = CHAT_EVENTS[event]

            # HACK?
            if hasattr(self.parser, "parse_" + event):
                data = getattr(self.parser, "parse_" + event)(data)

            await self.handle(event, data)

    async def handle_constellation(self, packet):
        """Handle constellation packets."""

        if "data" not in packet:
            return
        data = packet["data"]["payload"]

        scope, _, event = packet["data"]["channel"].split(":")
        event = scope + ':' + event

        if event in CONSTELLATION_EVENTS:
            event = CONSTELLATION_EVENTS[event]

            # HACK
            if hasattr(self.parser, "parse_" + event):
                data = getattr(self.parser, "parse_" + event)(data)

            await self.handle(event, data)

    async def handle(self, event, data):
        """Handle event."""

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
                    user_id = (await self.api.get_channel(
                        response.user, fields="userId"
                    ))["userId"]
                    await self.api.update_roles(user_id, ["Banned"], [])

    async def send(self, *args, **kwargs):
        """Send a packet to Mixer."""

        if self.chat is None:
            raise ConnectionError("Chat not initialized.")

        await self.chat.send(*args, **kwargs)
