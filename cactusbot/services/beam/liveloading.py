"""Interact with Beam liveloading."""

from logging import getLogger

import asyncio

from itertools import count

import re
import json

from aiohttp import ClientSession
from aiohttp.errors import ClientOSError, ServerDisconnectedError


class BeamLiveloading(ClientSession):
    """Interact with Beam liveloading."""

    URL = "wss://realtime.beam.pro/socket.io/?EIO=3&transport=websocket"

    RESPONSE_PATTERN = re.compile(r'^(?P<code>\d+)(?P<packet>.+)?$')
    EVENT_PATTERN = re.compile(r'^(?P<scope>[a-z]+):\d+:(?P<event>[a-z]+)')

    def __init__(self, channel, user):
        super().__init__()

        self.logger = getLogger(__name__)

        assert isinstance(channel, int), "Channel ID must be an integer."
        self.channel = channel

        assert isinstance(user, int), "User ID must be an integer."
        self.user = user

        self.websocket = None

    async def connect(self, *, base=2, maximum=60):
        """Connect to the liveloading server."""

        _backoff_count = count()

        while True:
            try:
                self.websocket = await super().ws_connect(self.URL)
            except ClientOSError:
                backoff = min(base**next(_backoff_count), maximum)
                self.logger.debug("Reconnecting in %s seconds...", backoff)
                await asyncio.sleep(backoff)
            else:
                await self.subscribe()
                self.logger.info("Connection established.")
                return self.websocket

    async def watch(self, handle=None):
        """Watch the liveloading websocket for incoming packets."""

        packet = await self.parse((await self.websocket.receive()).data)

        asyncio.ensure_future(self.ping(packet["data"]["pingInterval"]/1000))

        while True:
            response = (await self.websocket.receive()).data

            if isinstance(response, ServerDisconnectedError):
                self.logger.warning("Connection to liveloading server lost. "
                                    "Attempting to reconnect.")
                await self.connect()
            else:
                packet = await self.parse(response)

                self.logger.debug(packet)

                if callable(handle):
                    asyncio.ensure_future(handle(packet))

    async def subscribe(self, *interfaces):
        """Subscribe to liveloading interfaces."""

        if not interfaces:
            interfaces = (
                "channel:{channel}:update",
                "channel:{channel}:status",
                "channel:{channel}:followed",
                "channel:{channel}:subscribed",
                "user:{user}:followed",
                "user:{user}:subscribed",
                "user:{user}:achievement"
            )

        for interface in interfaces:
            interface = interface.format(
                channel=self.channel,
                user=self.user
            )
            packet = [
                "put",
                {
                    "method": "put",
                    "headers": {},
                    "data": {
                        "slug": [
                            interface
                        ]
                    },
                    "url": "/api/v1/live"
                }
            ]
            self.websocket.send_str('420' + json.dumps(packet))
            self.logger.debug("Subscribed to %s.", interface)

        self.logger.info("Successfully subscribed to liveloading interfaces.")

    async def ping(self, interval):
        """Periodically ping the liveloading server to sustain connection."""

        while True:
            self.websocket.send_str('2')
            self.logger.debug("Ping!")
            await asyncio.sleep(interval)

    async def parse(self, packet):
        """Parse a packet from liveloading."""

        match = re.match(self.RESPONSE_PATTERN, packet)

        data = match.group("packet")
        if data is not None:
            data = json.loads(data)

        return {
            "code": match.group("code"),
            "data": data
        }
