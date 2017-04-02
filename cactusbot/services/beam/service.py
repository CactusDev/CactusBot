"""Handle data from Beam."""

import asyncio

from ...packets import BanPacket, MessagePacket, Packet
from ...service import Service
from .api import BeamAPI
from .chat import BeamChat
from .constellation import BeamConstellation
from .parser import BeamParser


class BeamService(Service):
    """Handle data from Beam services."""

    PARSER = BeamParser

    CHAT_EVENTS = {
        "ChatMessage": ("message", PARSER.parse_message),
        "UserJoin": ("join", PARSER.parse_join),
        "UserLeave": ("leave", PARSER.parse_leave)
    }

    CONSTELLATION_EVENTS = {
        "channel:followed": ("follow", PARSER.parse_follow),
        "channel:subscribed": ("subscribe", PARSER.parse_subscribe),
        "channel:resubscribed": ("resubscribe", PARSER.parse_resubscribe),
        "channel:hosted": ("host", PARSER.parse_host)
    }

    def __init__(self, channel, token, handlers):

        super().__init__(handlers)

        self.api = BeamAPI(channel, token)

        self.parser = BeamParser()

        self.channel = channel

        self.chat = None
        self.constellation = None

    async def __aenter__(self):

        channel = await self.api.get_channel(self.channel)
        self.api.channel = str(channel["id"])

        user_id = channel["userId"]
        chat = await self.api.get_chat(channel["id"])
        assert "authkey" in chat, "Failed to authenticate with Beam"

        self.chat = BeamChat(channel["id"], *chat["endpoints"])
        self.constellation = BeamConstellation(channel["id"], user_id)

    async def run(self):
        """Connect to Beam chat and handle incoming packets."""

        bot_channel = await self.api.get_bot_channel()
        bot_id = bot_channel["channel"]["userId"]

        await self.handle(
            "username_update",
            Packet(username=bot_channel["channel"]["token"])
        )

        await self.chat.connect(bot_id, self.api.get_chat)
        asyncio.ensure_future(self.chat.read(self.handle_chat))

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

        if event in self.CHAT_EVENTS:

            event, parse = self.CHAT_EVENTS[event]
            data = parse(data)

            await self.handle(event, data)

    async def handle_constellation(self, packet):
        """Handle constellation packets."""

        if "data" not in packet:
            return
        data = packet["data"]["payload"]

        scope, _, event = packet["data"]["channel"].split(":")
        event = scope + ':' + event

        if event in self.CONSTELLATION_EVENTS:

            event, parse = self.CONSTELLATION_EVENTS[event]
            data = parse(data)

            await self.handle(event, data)

    async def respond(self, response):
        """Respond to a handled packet."""

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
        """Send a packet to Beam."""

        if self.chat is None:
            raise ConnectionError("Chat not initialized.")

        await self.chat.send(*args, **kwargs)
