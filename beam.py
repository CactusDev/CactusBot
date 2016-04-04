from tornado.websocket import websocket_connect
from tornado.gen import coroutine

from requests import Session
from requests.compat import urljoin

from logging import getLogger as get_logger
from logging import getLevelName as get_level_name
from logging import StreamHandler, FileHandler, Formatter

from time import gmtime

from functools import partial
from json import dumps, loads


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
        formatter.convert = gmtime

        try:
            from coloredlogs import ColoredFormatter
            colored_formatter = ColoredFormatter(format)
        except ImportError:
            colored_formatter = Formatter(format, datefmt='%Y-%m-%d %H:%M:%S')
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

        self.logger.debug("Connecting to: {server}".format(server=server))

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

    def send_message(self, arguments, method="msg"):
        """Send a message to a Beam chat through a websocket."""

        if isinstance(arguments, str):
            arguments = (arguments,)

        message_packet = {
            "type": "method",
            "method": method,
            "arguments": arguments,
            "id": self.message_id
        }

        if method == "whisper":
            self.logger.info("$ [{bot_name} > {user}] {message}".format(
                bot_name=self.config["auth"]["username"],
                user=arguments[0],
                message=arguments[1]))

        self.websocket.write_message(dumps(message_packet))
        self.message_id += 1

        return True

    def remove_message(self, channel_id, message_id):
        """Remove a message from chat."""
        return self._request("DELETE", "/chats/{id}/message/{message}".format(
            id=channel_id, message=message_id))

    @coroutine
    def read_chat(self, handler=None):
        while True:
            message = yield self.websocket.read_message()

            if message is None:
                self._on_connection_close()
                break
            else:
                response = loads(message)

            self.logger.debug(response)

            if callable(handler):
                handler(response)
