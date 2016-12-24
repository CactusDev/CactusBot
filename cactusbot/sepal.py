"""Interact with Sepal."""

import json
import logging
from .services.websocket import WebSocket


class Sepal(WebSocket):
    """Interact with Sepal."""

    def __init__(self, channel):
        super().__init__("wss://cactus.exoz.one/sepal")

        self.logger = logging.getLogger(__name__)

        self.channel = channel

    async def send(self, packet_type, **kwargs):
        """Send a packet to Sepal."""

        packet = {
            "type": packet_type,
            "channel": self.channel
        }

        packet.update(kwargs)
        await super().send(json.dumps(packet))

    async def initialize(self):
        """Send a subscribe packet."""

        await self.send("subscribe")

    async def parse(self, packet):
        """Parse a sepal packet."""

        try:
            packet = json.loads(packet)
        except (TypeError, ValueError):
            self.logger.exception("Invalid JSON: %s.", packet)
            return None
        else:
            self.logger.debug(packet)
            return packet
