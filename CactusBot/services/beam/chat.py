from logging import getLogger

from .api import BeamAPI

from websockets import connect
from websockets.exceptions import ConnectionClosed
from asyncio import sleep, ensure_future

from json import loads, dumps
from itertools import count, cycle


class BeamChat(object):

    def __init__(self, channel, api=None, **kwargs):
        # super().__init__(**kwargs)

        self.logger = getLogger(__name__)
        self.api = api or BeamAPI()

        self._channel = channel
        self.channel = kwargs.get("channel_data")

        self.chat = kwargs.get("chat")

        self._packet_counter = count()

    async def __aenter__(self):
        if self.channel is None:
            self.channel = await self.api.get_channel(self._channel)
        if self.chat is None:
            self.chat = await self.api.get_chat(self.channel["id"])

        assert self.chat.get("endpoints"), "Endpoints are required to connect!"
        self._address_counter = cycle(self.chat["endpoints"])

        self.websocket = await self._connect()

        return self

    async def __aexit__(self, *args, **kwargs):
        await self._conn.__aexit__(*args, **kwargs)

    def __await__(self, *args, **kwargs):
        return self.__aenter__().__await__()

    async def _connect(self):
        backoff = count()
        while True:
            try:
                self._conn = connect(self._chat_address)
                websocket = await self._conn.__aenter__()
            except ConnectionRefusedError:
                seconds = min(2**next(backoff), 60)
                self.logger.debug("Retrying in {} seconds...".format(seconds))
                await sleep(seconds)
            else:
                return websocket

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

    async def _authenticate(self, *auth):
        await self.send(self.channel["id"], *auth, method="auth", id="auth")

    async def read(self, handle=None):
        while True:
            try:
                response = await self.websocket.recv()
            except ConnectionClosed:
                self.logger.warning("Connection to chat server lost. "
                                    "Attempting to reconnect.")
                await self._connect()
                await self._authenticate()
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
    def _chat_address(self):
        return next(self._address_counter)
