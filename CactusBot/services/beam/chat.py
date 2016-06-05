"""BeamChat interacts with Beam chat servers."""

from logging import getLogger

from asyncio import sleep, ensure_future

from itertools import count, cycle

from json import loads, dumps

from websockets import connect
from websockets.exceptions import ConnectionClosed


class BeamChat(object):

    def __init__(self, channel: int, endpoints):

        self.logger = getLogger(__name__)

        self.channel = channel

        self._packet_counter = count()
        self._endpoint_cycle = cycle(endpoints)

    # async def __aenter__(self):
    #     # self.websocket = await self.connect()
    #     return self
    #
    # async def __aexit__(self, *args, **kwargs):
    #     await self._conn.__aexit__(*args, **kwargs)

    def __await__(self, *args, **kwargs):
        return self.__aenter__().__await__()

    async def connect(self, *auth, backoff=2):
        """Connect to a chat server."""
        _backoff_count = count()
        while True:
            try:
                self._conn = connect(self._endpoint)
                self.websocket = await self._conn.__aenter__()  # TODO: fix
            except ConnectionRefusedError:
                seconds = min(backoff**next(_backoff_count), 60)
                self.logger.debug("Retrying in %s seconds...", seconds)
                await sleep(seconds)
            else:
                await self.send(self.channel, *auth, method="auth", id="auth")
                return self.websocket

    async def send(self, *args, **kwargs):
        packet = {
            "type": "method",
            "method": "msg",
            "arguments": args,
            "id": kwargs.get("id") or self._packet_id
        }
        packet.update(kwargs)
        self.logger.debug(packet)
        await self.websocket.send(dumps(packet))

    async def read(self, handle=None):
        while True:
            try:
                response = await self.websocket.recv()
            except ConnectionClosed:
                self.logger.warning("Connection to chat server lost. "
                                    "Attempting to reconnect.")
                await self.connect()
                await self.authenticate()
            else:
                packet = loads(response)

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
