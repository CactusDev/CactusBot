"""Interact with Sepal."""

import json
import logging

from .api import CactusAPI
from .packets import MessagePacket
from .services.websocket import WebSocket


class Sepal(WebSocket):
    """Interact with Sepal."""

    def __init__(self, channel, service=None):
        super().__init__("wss://cactus.exoz.one/sepal")

        self.logger = logging.getLogger(__name__)

        self.channel = channel
        self.api = CactusAPI(channel)
        self.service = service
        self.parser = None

        if self.service is not None:
            self.parser = SepalParser(self.api)

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

        if not hasattr(self.parser, "parse_" + event):
            return

        data = await getattr(self.parser, "parse_" + event)(packet)

        await self.service.handle(event, data)


class SepalParser:
    """Parse Sepal packets."""

    def __init__(self, api):
        self.api = api

    async def parse_repeat(self, packet):
        """Parse the incoming repeat packet."""

        command_name = packet["data"]["commandName"]
        response = await self.api.get_command(command_name)

        if response.status is 404:
            return

        return MessagePacket.from_json(
            (await response.json())["data"]["attributes"]["response"])
