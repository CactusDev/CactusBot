"""Interact with WebSockets safely."""

import asyncio
import itertools
import logging

import aiohttp

_AIOHTTP_ERRORS = tuple(
    getattr(aiohttp.errors, error) for error in aiohttp.errors.__all__
)


class WebSocket(aiohttp.ClientSession):
    """Interact with WebSockets safely."""

    def __init__(self, *endpoints):
        super().__init__()

        self.logger = logging.getLogger(__name__)

        assert len(endpoints), "An endpoint is required to connect."

        self.websocket = None

        self._init_args = ()
        self._init_kwargs = {}

        self._endpoint_cycle = itertools.cycle(endpoints)

    async def connect(self, *args, base=2, maximum=60, **kwargs):
        """Connect to a WebSocket."""

        self._init_args = args
        self._init_kwargs = kwargs

        _backoff_count = itertools.count()
        self.logger.debug("Connecting...")

        while True:
            try:
                self.websocket = await self.ws_connect(self._endpoint)
            except _AIOHTTP_ERRORS:
                backoff = min(base**next(_backoff_count), maximum)
                self.logger.debug("Retrying in %s seconds...", backoff)
                await asyncio.sleep(backoff)
            else:
                await self.initialize(*args, **kwargs)
                self.logger.info("Connection established.")
                return self.websocket

    async def send(self, packet):
        """Send a packet to the WebSocket."""
        assert self.websocket is not None, "Must connect to send."
        self.logger.debug(packet)
        self.websocket.send_str(packet)

    async def receive(self):
        """Receive a packet from the WebSocket."""
        return (await self.websocket.receive()).data

    async def read(self, handle):
        """Read packets from the WebSocket."""

        assert self.websocket is not None, "Must connect to read."
        assert callable(handle), "Handler must be callable."

        while True:
            packet = await self.receive()
            if isinstance(packet, str):
                packet = await self.parse(packet)
                if packet is not None:
                    asyncio.ensure_future(handle(packet))
            else:
                self.logger.warning("Connection lost. Reconnecting.")
                await self.connect(*self._init_args, **self._init_kwargs)

    async def initialize(self):
        """Run initialization procedure."""
        pass

    async def parse(self, packet):
        """Parse a packet from the WebSocket."""
        return packet

    @property
    def _endpoint(self):
        return next(self._endpoint_cycle)
