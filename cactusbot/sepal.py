"""Interact with Sepal."""

import json
import logging

from .packets import MessagePacket, Packet
from .services.websocket import WebSocket


class Sepal(WebSocket):
    """Interact with Sepal."""

    def __init__(self, channel, service=None):
        super().__init__("wss://cactus.exoz.one/sepal")

        self.logger = logging.getLogger(__name__)

        self.channel = channel
        self.service = service
        self.parser = SepalParser()

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
        """Parse a Sepal packet."""

        try:
            packet = json.loads(packet)
        except (TypeError, ValueError):
            self.logger.exception("Invalid JSON: %s.", packet)
            return None
        else:
            self.logger.debug(packet)
            return packet

    async def handle(self, packet):
        """Convert a JSON packet to a CactusBot packet."""

        assert self.service is not None, "Must have a service to handle"

        if "event" not in packet:
            return

        event = packet["event"]

        if not hasattr(self.parser, "parse_" + event.lower()):
            return

        data = await getattr(self.parser, "parse_" + event)(packet)

        if isinstance(data, (list, tuple)):
            for packet in data:
                await self.service.handle(event, packet)
        else:
            await self.service.handle(event, data)


class SepalParser:
    """Parse Sepal packets."""

    async def parse_repeat(self, packet):
        """Parse the incoming repeat packets."""

        return MessagePacket.from_json(packet["data"]["response"])

    async def parse_config(self, packet):
        """Parse the incoming config packets."""

        return [Packet("config", key=key, values=values)
                for key, values in packet["data"].items()]
