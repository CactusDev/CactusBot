"""Interact with Beam chat."""

from logging import getLogger

import asyncio

from itertools import count, cycle

import json

from aiohttp import ClientSession
from aiohttp.errors import ClientOSError, ServerDisconnectedError


class BeamChat(ClientSession):
    """Interact with Beam chat."""

    def __init__(self, channel, *endpoints):
        super().__init__()

        self.logger = getLogger(__name__)

        assert isinstance(channel, int), "Channel ID must be an integer."
        self.channel = channel

        assert len(endpoints), "An endpoint is required to connect."

        self.websocket = None

        self._packet_counter = count()
        self._endpoint_cycle = cycle(endpoints)

    async def connect(self, *auth, base=2, maximum=60):
        """Connect to a chat server."""

        _backoff_count = count()

        while True:
            try:
                self.websocket = await super().ws_connect(self._endpoint)
            except ClientOSError:
                backoff = min(base**next(_backoff_count), maximum)
                self.logger.debug("Retrying in %s seconds...", backoff)
                await asyncio.sleep(backoff)
            else:
                await self.authenticate(*auth)
                self.logger.info("Connection established.")
                return self.websocket

    async def send(self, *args, **kwargs):
        """Send a packet to chat."""

        if self.websocket is None:
            raise ConnectionError("Not connected. Run connect() first!")

        packet = {
            "type": "method",
            "method": "msg",
            "arguments": args,
            "id": kwargs.get("id") or self._packet_id
        }

        packet.update(kwargs)

        self.logger.debug(packet)

        self.websocket.send_str(json.dumps(packet))

    async def read(self, handle=None):
        """Read and parse packets from chat."""

        if self.websocket is None:
            raise ConnectionError("Not connected. Run connect() first!")

        while True:
            response = (await self.websocket.receive()).data

            if isinstance(response, ServerDisconnectedError):
                self.logger.warning("Connection to chat server lost. "
                                    "Attempting to reconnect.")
                await self.connect()
            else:
                packet = json.loads(response)

                if packet.get("error") is not None:
                    self.logger.error(packet)
                else:
                    self.logger.debug(packet)

                if callable(handle):
                    asyncio.ensure_future(handle(packet))

    async def authenticate(self, *auth):
        """Send an authentication packet to chat."""

        await self.send(self.channel, *auth, method="auth", id="auth")
        return True

    @property
    def _packet_id(self):
        return next(self._packet_counter)

    @property
    def _endpoint(self):
        return next(self._endpoint_cycle)
