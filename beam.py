from tornado.websocket import websocket_connect
from tornado.gen import coroutine
from tornado.ioloop import PeriodicCallback

from requests import Session
from requests.compat import urljoin

from logging import getLogger as get_logger
from logging import getLevelName as get_level_name
from logging import StreamHandler, FileHandler, Formatter

from functools import partial
from json import dumps, loads

from re import match


class Beam:
    path = "https://beam.pro/api/v1/"

    message_id = 0

    def __init__(self, debug="INFO", **kwargs):
        self._init_logger(debug, kwargs.get("log_to_file", True))
        self.http_session = Session()

    def _init_logger(self, level="INFO", file_logging=True, **kwargs):
        """Initialize logger."""

        self.logger = get_logger("CactusBot")
        self.logger.propagate = False

        self.logger.setLevel("DEBUG")

        if level is True:
            level = "DEBUG"
        elif level is False:
            level = "WARNING"
        elif hasattr(level, "upper"):
            level = level.upper()

        format = kwargs.get(
            "format",
            "%(asctime)s %(name)s %(levelname)-8s %(message)s"
        )

        formatter = Formatter(format, datefmt='%Y-%m-%d %H:%M:%S')

        try:
            from coloredlogs import ColoredFormatter
            colored_formatter = ColoredFormatter(format)
        except ImportError:
            colored_formatter = formatter
            self.logger.warning(
                "Module 'coloredlogs' unavailable; using ugly logging.")

        stream_handler = StreamHandler()
        stream_handler.setLevel(level)
        stream_handler.setFormatter(colored_formatter)
        self.logger.addHandler(stream_handler)

        if file_logging:
            file_handler = FileHandler("latest.log")
            file_handler.setLevel("DEBUG")
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

        get_logger("requests").setLevel(get_level_name("WARNING"))

        self.logger.info("Logger initialized with level '{}'.".format(level))

    def _request(self, url, method="GET", **kwargs):
        """Send HTTP request to Beam."""
        return self.http_session.request(
            method, urljoin(self.path, url.lstrip('/')), **kwargs).json()

    def login(self, username, password, code=''):
        """Authenticate and login with Beam."""
        packet = {
            "username": username,
            "password": password,
            "code": code
        }
        return self._request("/users/login", "POST", data=packet)

    def get_channel(self, id, **params):
        """Get channel data by username."""
        return self._request("/channels/{id}".format(id=id), params=params)

    def get_chat(self, id):
        """Get chat server data."""
        return self._request("/chats/{id}".format(id=id))

    def connect(self, channel_id, bot_id):
        """Connect to a Beam chat through a websocket."""

        chat = self.get_chat(channel_id)
        server = chat["endpoints"][0]
        authkey = chat["authkey"]

        self.logger.debug("Connecting to: {server}.".format(server=server))

        websocket_connection = websocket_connect(server)
        websocket_connection.add_done_callback(
            partial(self.authenticate, channel_id, bot_id, authkey))

    def authenticate(self, channel_id, bot_id, authkey, future):
        if future.exception() is None:
            self.websocket = future.result()
            self.logger.info("Successfully connected to chat {}.".format(
                self.channel_data["token"]))

            self.send_message((channel_id, bot_id, authkey), method="auth")

            self.read_chat(self.handle)
        else:
            raise ConnectionError(future.exception())

    def send_message(self, *messages, method="msg"):
        """Send a message to a Beam chat through a websocket."""

        for message in messages:
            if isinstance(message, str):
                message = (message,)

            message_packet = {
                "type": "method",
                "method": method,
                "arguments": message,
                "id": self.message_id
            }

            if method == "whisper":
                self.logger.info("$ [{bot_name} > {user}] {message}".format(
                    bot_name=self.config["auth"]["username"],
                    user=message[0],
                    message=message[1]))

            self.websocket.write_message(dumps(message_packet))
            self.message_id += 1

    def remove_message(self, channel_id, message_id):
        """Remove a message from chat."""
        return self._request("DELETE", "/chats/{id}/message/{message}".format(
            id=channel_id, message=message_id))

    @coroutine
    def read_chat(self, handler=None):
        while True:
            message = yield self.websocket.read_message()

            if message is None:
                raise ConnectionError

            response = loads(message)

            self.logger.debug("CHAT: {}".format(response))

            if callable(handler):
                handler(response)

    def connect_to_liveloading(self, channel_id, user_id):
        liveloading_websocket_connection = websocket_connect(
            "wss://realtime.beam.pro/socket.io/?EIO=3&transport=websocket")
        liveloading_websocket_connection.add_done_callback(
            partial(self.subscribe_to_liveloading, channel_id, user_id))

    def subscribe_to_liveloading(self, channel_id, user_id, future):
        if future.exception() is None:
            self.liveloading_websocket = future.result()

            self.logger.info(
                "Successfully connected to liveloading websocket.")

            interfaces = (
                "channel:{channel_id}:update",
                "channel:{channel_id}:followed",
                "channel:{channel_id}:subscribed",
                "channel:{channel_id}:resubscribed",
                "user:{user_id}:update"
            )
            self.subscribe_to_interfaces(
                *tuple(
                    interface.format(channel_id=channel_id, user_id=user_id)
                    for interface in interfaces
                )
            )

            self.logger.info(
                "Successfully subscribed to liveloading interfaces.")

            self.watch_liveloading()
        else:
            raise ConnectionError(future.exception())

    def subscribe_to_interfaces(self, *interfaces):
        for interface in interfaces:
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
            self.liveloading_websocket.write_message('420' + dumps(packet))

    def parse_liveloading_message(self, message):
        sections = match("(\d+)(.+)?$", message).groups()

        return {
            "code": sections[0],
            "data": loads(sections[1]) if sections[1] is not None else None
        }

    @coroutine
    def watch_liveloading(self, handler=None):

        response = yield self.liveloading_websocket.read_message()
        if response is None:
            raise ConnectionError

        packet = self.parse_liveloading_message(response)

        PeriodicCallback(
            partial(self.liveloading_websocket.write_message, '2'),
            packet["data"]["pingInterval"]
        ).start()

        while True:
            message = yield self.liveloading_websocket.read_message()

            if message is None:
                raise ConnectionError

            packet = self.parse_liveloading_message(message)

            if packet.get("data") is not None:
                self.logger.debug("LIVE: {}".format(packet))

            if isinstance(packet["data"], list):
                if isinstance(packet["data"][0], str):
                    if packet["data"][1].get("following"):
                        self.logger.info("- {} followed.".format(
                            packet["data"][1]["user"]["username"]))
                        self.send_message(
                            "Thanks for the follow, @{}!".format(
                                packet["data"][1]["user"]["username"]))
                    elif packet["data"][1].get("subscribed"):
                        self.logger.info("- {} subscribed.".format(
                            packet["data"][1]["user"]["username"]))
                        self.send_message(
                            "Thanks for the subscription, @{}! <3".format(
                                packet["data"][1]["user"]["username"]))
