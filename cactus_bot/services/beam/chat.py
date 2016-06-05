"""Interacts with Beam chat servers."""

from logging import getLogger

from asyncio import sleep, ensure_future

from itertools import count, cycle

from json import loads, dumps

from aiohttp import ClientSession
from websockets.exceptions import ConnectionClosed


class BeamChat(ClientSession):
    """Interact with Beam chat."""

    def __init__(self, channel: int, *endpoints):
        super().__init__()

        self.logger = getLogger(__name__)

        self.channel = channel

        self._packet_counter = count()
        self._endpoint_cycle = cycle(endpoints)

    async def connect(self, *auth, backoff=2):
        """Connect to a chat server."""
        _backoff_count = count()
        while True:
            try:
                self.websocket = await super().ws_connect(self._endpoint)
            except ConnectionRefusedError:
                seconds = min(backoff**next(_backoff_count), 60)
                self.logger.debug("Retrying in %s seconds...", seconds)
                await sleep(seconds)
            else:
                await self.authenticate(*auth)
                return self.websocket

    async def authenticate(self, *auth):
        """Send an authentication packet to chat."""

        await self.send(self.channel, *auth, method="auth", id="auth")
        return True

    async def send(self, *args, **kwargs):
        """Send a packet to chat."""

        packet = {
            "type": "method",
            "method": "msg",
            "arguments": args,
            "id": kwargs.get("id") or self._packet_id
        }

        packet.update(kwargs)

        self.logger.debug(packet)

        self.websocket.send_str(dumps(packet))

    async def read(self, handle=None):
        """Read and parse packets from chat."""

        while True:

            try:
                response = await self.websocket.receive()
            except ConnectionClosed:
                self.logger.warning("Connection to chat server lost. "
                                    "Attempting to reconnect.")
                await self.connect()
            else:
                packet = loads(response.data)

                if packet.get("error") is not None:
                    self.logger.error(packet)
                else:
                    self.logger.debug(packet)

                if callable(handle):
                    ensure_future(handle(packet))

    @property
    def _packet_id(self):
        return next(self._packet_counter)

    @property
    def _endpoint(self):
        return next(self._endpoint_cycle)
