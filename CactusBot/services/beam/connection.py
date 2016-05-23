from logging import getLogger

from websockets import connect
from websockets.exceptions import ConnectionClosed
from asyncio import sleep

from requests import Session
from requests.compat import urljoin

# from functools import partial
from json import dumps, loads
from itertools import count, cycle

# from re import match

from .api import BeamAPI
from .parser import BeamHandler


class Beam(BeamHandler):

    path = "https://beam.pro/api/v1/"

    def __init__(self, username, password, channel, **kwargs):
        super().__init__(username, password, **kwargs)

        self.logger = getLogger(__name__)

        self.http_session = Session()

        self.channel = channel
        self.channel_data = self.get_channel(self.channel)

        self.auth = {
            "username": username,
            "password": password,
            "code": kwargs.get("code", '')
        }

        self.data = self._login(**self.auth)
        self.chat = self.get_chat(self.channel_data["id"])

        self._packet_counter = count()
        self._address_counter = cycle(self.chat["endpoints"])

    async def __aenter__(self):
        await self._connect()
        return self

    async def _connect(self):
        backoff = count()
        while True:
            try:
                self._conn = connect(self._chat_address)
                self.websocket = await self._conn.__aenter__()
            except ConnectionRefusedError:
                seconds = min(2**next(backoff), 60)
                self.logger.info("Retrying in {} seconds...".format(seconds))
                await sleep(seconds)
            else:
                break

    async def __aexit__(self, *args, **kwargs):
        await self._conn.__aexit__(*args, **kwargs)

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

    async def _authenticate(self):
        await self.send(
            self.channel_data["id"], self.data["id"], self.chat["authkey"],
            method="auth", id="auth"
        )

    async def read(self):
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

            await self.handle(packet)

    @property
    def _packet_id(self):
        return next(self._packet_counter)

    @property
    def _chat_address(self):
        return next(self._address_counter)

    def _request(self, url, method="GET", **kwargs):
        """Send HTTP request to Beam."""
        response = self.http_session.request(
            method, urljoin(self.path, url.lstrip('/')), **kwargs)
        try:
            return response.json()
        except Exception:
            return response.text

    def _login(self, username, password, code=''):
        """Authenticate and login with Beam."""
        packet = {
            "username": username,
            "password": password,
            "code": code
        }
        return self._request("/users/login", method="POST", data=packet)

    def get_channel(self, id, **params):  # Add explosions
        """Get channel data by username."""
        return self._request("/channels/{id}".format(id=id), params=params)

    def get_chat(self, id):  # Add explosions
        """Get chat server data."""
        return self._request("/chats/{id}".format(id=id))

    def remove_message(self, channel_id, message_id):
        """Remove a message from chat."""
        return self._request("/chats/{id}/message/{message}".format(
            id=channel_id, message=message_id), method="DELETE")
#
# @coroutine
# def read_chat(self, handler=None):
#     """Read and handle messages from a Beam chat through a websocket."""
#
#     while True:
#         message = yield self.websocket.read_message()
#
#         if message is None:
#             self.logger.warning(
#                 "Connection to chat server lost. Attempting to reconnect.")
#             self.server_offset += 1
#             self.server_offset %= len(self.servers)
#             self.logger.debug("Connecting to: {server}.".format(
#                 server=self.servers[self.server_offset]))
#
#             websocket_connection = websocket_connect(
#                 self.servers[self.server_offset])
#
#             authkey = self.get_chat(
#                 self.connection_information["channel_id"])["authkey"]
#
#             if self.connection_information["silent"]:
#                 return websocket_connection.add_done_callback(
#                     partial(
#                         self.authenticate,
#                         self.connection_information["channel_id"]
#                     )
#                 )
#             else:
#                 return websocket_connection.add_done_callback(
#                     partial(
#                         self.authenticate,
#                         self.connection_information["channel_id"],
#                         self.connection_information["bot_id"],
#                         authkey
#                     )
#                 )
#
#         else:
#             response = loads(message)
#
#             self.logger.debug("CHAT: {}".format(response))
#
#             if callable(handler):
#                 handler(response)
#
# def connect_to_liveloading(self, channel_id, user_id):
#     """Connect to Beam liveloading."""
#
#     self.liveloading_connection_information = {
#         "channel_id": channel_id,
#         "user_id": user_id
#     }
#
#     liveloading_websocket_connection = websocket_connect(
#         "wss://realtime.beam.pro/socket.io/?EIO=3&transport=websocket")
#     liveloading_websocket_connection.add_done_callback(
#         partial(self.subscribe_to_liveloading, channel_id, user_id))
#
# def subscribe_to_liveloading(self, channel_id, user_id, future):
#     """Subscribe to Beam liveloading."""
#
#     if future.exception() is None:
#         self.liveloading_websocket = future.result()
#
#         self.logger.info(
#             "Successfully connected to liveloading websocket.")
#
#         interfaces = (
#             "channel:{channel_id}:update",
#             "channel:{channel_id}:followed",
#             "channel:{channel_id}:subscribed",
#             "channel:{channel_id}:resubscribed",
#             "user:{user_id}:update"
#         )
#         self.subscribe_to_interfaces(
#             *tuple(
#                 interface.format(channel_id=channel_id, user_id=user_id)
#                 for interface in interfaces
#             )
#         )
#
#         self.logger.info(
#             "Successfully subscribed to liveloading interfaces.")
#
#         self.watch_liveloading()
#     else:
#         raise ConnectionError(future.exception())
#
# def subscribe_to_interfaces(self, *interfaces):
#     """Subscribe to a Beam liveloading interface."""
#
#     for interface in interfaces:
#         packet = [
#             "put",
#             {
#                 "method": "put",
#                 "headers": {},
#                 "data": {
#                     "slug": [
#                         interface
#                     ]
#                 },
#                 "url": "/api/v1/live"
#             }
#         ]
#         self.liveloading_websocket.write_message('420' + dumps(packet))
#
# def parse_liveloading_message(self, message):
#     """Parse a message received from the Beam liveloading websocket."""
#
#     sections = match("(\d+)(.+)?$", message).groups()
#
#     return {
#         "code": sections[0],
#         "data": loads(sections[1]) if sections[1] is not None else None
#     }
#
# # @coroutine
# def watch_liveloading(self, handler=None):
#     """Watch and handle packets from the Beam liveloading websocket."""
#
#     response = yield self.liveloading_websocket.read_message()
#     if response is None:
#         raise ConnectionError
#
#     packet = self.parse_liveloading_message(response)
#
#     PeriodicCallback(
#         partial(self.liveloading_websocket.write_message, '2'),
#         packet["data"]["pingInterval"]
#     ).start()
#
#     while True:
#         message = yield self.liveloading_websocket.read_message()
#
#         if message is None:
#             self.logger.warning("Connection to liveloading server lost. "
#                                 "Attempting to reconnect.")
#             return self.connect_to_liveloading(
#                 **self.liveloading_connection_information)
#
#         packet = self.parse_liveloading_message(message)
#
#         if packet.get("data") is not None:
#             self.logger.debug("LIVE: {}".format(packet))
#
#         # TODO: move to handler
#         if isinstance(packet["data"], list):
#             if isinstance(packet["data"][0], str):
#                 if packet["data"][1].get("following"):
#                     self.logger.info("- {} followed.".format(
#                         packet["data"][1]["user"]["username"]))
#                     self.send_message(
#                         "Thanks for the follow, @{}!".format(
#                             packet["data"][1]["user"]["username"]))
#                 elif packet["data"][1].get("subscribed"):
#                     self.logger.info("- {} subscribed.".format(
#                         packet["data"][1]["user"]["username"]))
#                     self.send_message(
#                         "Thanks for the subscription, @{}! <3".format(
#                             packet["data"][1]["user"]["username"]))
