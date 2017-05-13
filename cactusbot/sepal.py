"""Interact with Sepal."""

import json
import logging

from .packets import MessagePacket, Packet
from .services.websocket import WebSocket


class Sepal(WebSocket):
    """Interact with Sepal."""

    URL = "wss://cactus.exoz.one/sepal"

    def __init__(self, channel, service, url=URL):
        super().__init__(url)

        self.logger = logging.getLogger(__name__)

        self.channel = channel
        self.service = service

    async def send(self, packet_type, **kwargs):
        """Send a packet to Sepal."""

        packet = {
            "type": packet_type,
            "data": {
                "channel": self.channel
            }
        }

        packet.update(kwargs)
        await self._send(json.dumps(packet))

    async def initialize(self, *_):
        """Send a subscribe packet."""

        await self.send("join")

    async def _success_function(self, packet):
        self.logger.debug(packet)
        return packet
    parse = WebSocket._parse_json(_success_function)

    async def handle(self, packet):
        """Convert a JSON packet to a CactusBot packet."""

        assert self.service is not None, "Must have a service to handle"

        event = packet.get("event")

        if event not in PARSERS:
            return

        data = await PARSERS[event](packet)

        if data is None:
            return

        if isinstance(data, (list, tuple)):
            for _packet in data:
                await self.service.handle(event, _packet)
        else:
            await self.service.handle(event, data)


async def parse_repeat(packet):
    """Parse the incoming repeat packets."""

    if "message" in packet["data"]:
        return MessagePacket.from_json(packet["data"])


async def parse_config(packet):
    """Parse the incoming config packets."""

    return [
        Packet("announce", **packet["data"]["announce"]),
        Packet("spam", **packet["data"]["spam"]),
        Packet("whitelistedUrls", urls=packet["data"]["whitelistedUrls"])
    ]

PARSERS = {
    "repeat": parse_repeat,
    "config": parse_config
}
