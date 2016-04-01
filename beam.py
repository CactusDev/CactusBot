from tornado.websocket import websocket_connect
from tornado.gen import coroutine

from requests import Session

from logging import getLogger as get_logger
from logging import INFO, WARNING, FileHandler

from functools import partial
from json import dumps, loads


class Beam:
    path = "https://beam.pro/api/v1"

    message_id = 0

    def __init__(self, debug="WARNING", **kwargs):
        self._init_logger(debug, kwargs.get("log_to_file", True))
        self.http_session = Session()

    def _init_logger(self, level, log_to_file=True):
        """Initialize logger."""

        self.logger = get_logger("CactusBot")

        if log_to_file:
            file_handler = FileHandler("latest.log")
            file_handler.setLevel(INFO)
            self.logger.addHandler(file_handler)

        if level is True:
            level = "DEBUG"
        elif level is False:
            level = "WARNING"

        level = level.upper()

        levels = ("CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "NOTSET")
        if level in levels:
            level_num = __import__("logging").__getattribute__(level)
            self.logger.setLevel(level_num)
            get_logger("requests").setLevel(WARNING)
            self.logger.info("Logger level set to: {}".format(level))

            try:
                from coloredlogs import install
                install(level=level)
            except ImportError:
                self.logger.warning(
                    "Module 'coloredlogs' unavailable; using ugly logging.")
        else:
            self.logger.warn("Invalid logger level: {}".format(level))

        self.logger.info("Logger initialized!")

    def _request(self, req, url, **kwargs):
        """Send HTTP request to Beam."""
        if req.lower() in ("get", "head", "post", "put", "delete", "options"):
            if req.lower() == "get":
                response = self.http_session.get(
                    self.path + url,
                    params=kwargs.get("params")
                )
            else:
                response = self.http_session.__getattribute__(req.lower())(
                    self.path + url,
                    data=kwargs.get("data")
                )

            try:
                json = response.json()
            except ValueError:
                return None
            else:
                if "error" in json.keys():
                    self.logger.warn("Error: {}".format(json["error"]))
                return json
        else:
            self.logger.debug("Invalid request: {}".format(req))

    def login(self, username, password, code=''):
        """Authenticate and login with Beam."""
        packet = {
            "username": username,
            "password": password,
            "code": code
        }
        return self._request("POST", "/users/login", data=packet)

    def get_channel(self, id, **p):
        """Get channel data by username."""
        return self._request("GET", "/channels/{id}".format(id=id), params=p)

    def get_chat(self, id):
        """Get chat server data."""
        return self._request("GET", "/chats/{id}".format(id=id))

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
