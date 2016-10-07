"""Interact with Beam Constellation."""

from logging import getLogger

import re
import json

import asyncio

from .. import WebSocket


class BeamConstellation(WebSocket):
    """Interact with Beam Constellation."""

    URL = "wss://constellation.beam.pro"

    RESPONSE_EXPR = re.compile(r'^(\d+)(.+)?$')
    INTERFACE_EXPR = re.compile(r'^([a-z]+):\d+:([a-z]+)')

    def __init__(self, channel, user):
        super().__init__(self.URL)

        self.logger = getLogger(__name__)

        assert isinstance(channel, int), "Channel ID must be an integer."
        self.channel = channel

        assert isinstance(user, int), "User ID must be an integer."
        self.user = user

    async def read(self, handle):
        """Read packets from the Constellation WebSocket."""

        packet = await self.parse(await self.receive())

        await super().read(handle)

    async def initialize(self, *interfaces):
        """Subscribe to Constellation interfaces."""

        if not interfaces:
            interfaces = [
                "channel:{channel}:update",
                "channel:{channel}:status",
                "channel:{channel}:followed",
                "channel:{channel}:subscribed",
                "channel:{channel}:hosted",
                "user:{user}:followed",
                "user:{user}:subscribed",
                "user:{user}:achievement"
            ]
            interfaces = list(
                interface.format(channel=self.channel, user=self.user)
                for interface in interfaces
            )

        packet = {
            "type": "method",
            "method": "livesubscribe",
            "params": {
                "events": interfaces
            },
            "id": 1
        }

        self.websocket.send_str(json.dumps(packet))

        self.logger.info(
            "Successfully subscribed to Constellation interfaces.")
