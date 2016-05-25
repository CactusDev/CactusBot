from logging import getLogger

from .api import BeamAPI

from websockets import connect
from websockets.exceptions import ConnectionClosed
from asyncio import sleep

from json import loads, dumps
from itertools import count, cycle


class BeamChat(BeamAPI):

    def __init__(self, channel, **kwargs):
        super().__init__(**kwargs)

        self.logger = getLogger(__name__)

        self.channel = channel
        self.channel_data = dict()

        self._packet_counter = count()

    async def __aenter__(self):
        # TODO: insta-efficiency. just add logic!
        self.channel_data = await self.get_channel(self.channel)
        self.chat = await self.get_chat(self.channel_data["id"])
        self._address_counter = cycle(self.chat["endpoints"])

        await self._connect()
        return self

    async def __aexit__(self, *args, **kwargs):
        await self._conn.__aexit__(*args, **kwargs)

    async def _connect(self):
        backoff = count()
        while True:
            try:
                self._conn = connect(self._chat_address)
                self.websocket = await self._conn.__aenter__()
            except ConnectionRefusedError:
                seconds = min(2**next(backoff), 60)
                self.logger.debug("Retrying in {} seconds...".format(seconds))
                await sleep(seconds)
            else:
                return True

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
        await self.send(
            self.channel_data["id"], *auth, method="auth", id="auth"
        )

    async def read(self, handle=None):
        while True:
            try:
                response = await self.websocket.recv()
            except ConnectionClosed:
                self.logger.warning("Connection to chat server lost. "
                                    "Attempting to reconnect.")
                await self._connect()
                await self._authenticate(self.channel)
            else:
                packet = loads(response)

                if packet.get("error") is not None:
                    self.logger.error(packet)
                else:
                    self.logger.debug(packet)

                if callable(handle):
                    await handle(packet)

    @property
    def _packet_id(self):
        return next(self._packet_counter)

    @property
    def _chat_address(self):
        return next(self._address_counter)
