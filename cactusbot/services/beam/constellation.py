"""Interact with Beam Constellation."""

import re
import json

from .. import WebSocket


class BeamConstellation(WebSocket):
    """Interact with Beam Constellation."""

    URL = "wss://constellation.beam.pro"

    RESPONSE_EXPR = re.compile(r'^(\d+)(.+)?$')
    INTERFACE_EXPR = re.compile(r'^([a-z]+):\d+:([a-z]+)')

    def __init__(self, channel, user):
        super().__init__(self.URL)

        assert isinstance(channel, int), "Channel ID must be an integer."
        self.channel = channel

        assert isinstance(user, int), "User ID must be an integer."
        self.user = user

    async def initialize(self, *interfaces):
        """Subscribe to Constellation interfaces."""

        if not interfaces:
            interfaces = (
                "channel:{channel}:update",
                "channel:{channel}:status",
                "channel:{channel}:followed",
                "channel:{channel}:subscribed",
                "channel:{channel}:resubscribed",
                "channel:{channel}:hosted",
                "user:{user}:followed",
                "user:{user}:subscribed",
                "user:{user}:achievement"
            )

            interfaces = [
                interface.format(channel=self.channel, user=self.user)
                for interface in interfaces
            ]

        packet = {
            "type": "method",
            "method": "livesubscribe",
            "params": {
                "events": interfaces
            },
            "id": 1
        }

        self.websocket.send_str(json.dumps(packet))
        await self.receive()

        self.logger.info(
            "Successfully subscribed to Constellation interfaces.")

    async def parse(self, packet):
        """Parse a chat packet."""

        try:
            packet = json.loads(packet)
        except (TypeError, ValueError):
            self.logger.exception("Invalid JSON: %s.", packet)
            return None
        else:
            if packet.get("error") is not None:
                self.logger.error(packet)
            else:
                self.logger.debug(packet)
            return packet
