from logging import getLogger as get_logger
from requests import Session
from json import dumps, loads
import websockets
import asyncio
from messages import *


class User:
    path = "https://beam.pro/api/v1"

    def __init__(self, debug="WARNING", **kwargs):
        self._init_logger(debug)
        self.session = Session()
        self.path = "https://beam.pro/api/v1"

    def _init_logger(self, level):
        """Initialize logger."""

        self.logger = get_logger('CactusBot')

        if level is True:
            level = "DEBUG"
        elif level is False:
            level = "WARNING"

        levels = ("CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "NOTSET")
        if level.upper() in levels:
            level_num = __import__("logging").__getattribute__(level.upper())
            self.logger.setLevel(level_num)
            self.logger.info("Logger level set to: {}".format(level.upper()))

            try:
                from coloredlogs import install
                install(level=level.upper())
            except ImportError:
                self.logger.warning(
                    "Module 'coloredlogs' unavailable; using ugly logging.")
        else:
            self.logger.warn("Invalid logger level: {}".format(level.upper()))

        self.logger.info("Logger initialized!")

    def request(self, req, url, **kwargs):
        """Send HTTP request to Beam."""
        if req.lower() in ('get', 'head', 'post', 'put', 'delete', 'options'):
            if req.lower() == "get":
                response = self.session.get(
                    self.path + url,
                    params=kwargs["params"]
                )
            else:
                response = self.session.__getattribute__(req.lower())(
                    self.path + url,
                    data=kwargs["data"]
                )

            if 'error' in response.json().keys():
                self.logger.warn("Error: {}".format(response.json()['error']))

            return response.json()
        else:
            self.logger.debug("Invalid request: {}".format(req))

    def login(self, username, password, code=''):
        """Authenticate and login with Beam."""
        l = locals()
        packet = {n: l[n] for n in ("username", "password", "code")}
        return self.request("POST", "/users/login", data=packet)

    def get_channel(self, id, **p):
        """Get channel data by username."""
        return self.request("GET", "/channels/{id}".format(id=id), params=p)

    def get_chat(self, id):
        """Get chat server data."""
        return self.request("GET", "/chats/{id}".format(id=id), params="")

    def send_message(self, arguments, method="msg"):
        if isinstance(arguments, str):
            arguments = [arguments]

        msg_packet = {
            "type": "method",
            "method": method,
            "arguments": arguments,
            "id": self.msg_id
        }

        yield from self.websocket.send(dumps(msg_packet))
        self.msg_id += 1

        ret = yield from self.websocket.recv()

        return ret

    def connect(self, channel_id, bot_id):
        # Get the channel ID from the channel name
        self.chan_id = self.get_channel(channel_id, fields="id")["id"]
        # Get the chat information from the channel ID
        self.chat = self.get_chat(self.chan_id)
        # Get the server address from the chat info
        self.server = self.chat["endpoints"][0]
        # Get the authkey we need to authenticate to the server
        self.authkey = self.chat["authkey"]

        self.logger.debug("Connecting to: {server}".format(server=self.server))

        # Need to get the server to connect to
        self.websocket = yield from websockets.connect(self.server)

        ret = yield from self.send_message([self.chan_id, bot_id, self.authkey], method="auth")

        try:
            ret = loads(ret)
        except ValueError as e:
            self.logger.error("JSON failure during login")
            self.logger.error(e)
            quit()

        # Did we authenticate correctly?
        if ret["data"]["authenticated"]:
            self.logger.info("Authenticated successfully!")
            # We'll get a Message sent packet back in the websocket,
            # make sure to clear that from WS before moving on
            ret = yield from self.websocket.recv()
            self.logger.info(ret)

            return self.websocket
        else:
            self.logger.warn("Failed to authenticate")
            self.logger.info(response)
            yield from self.websocket.recv()
            return False

    def read_chat(self):

        while True:
            try:
                msg = yield from self.websocket.recv()
                msg = loads(msg)

                if "event" not in msg:
                    self.logger.warning("No event key in message")
                    self.logger.warning(msg)
                else:
                    switch = {
                        "ChatMessage": message_handler,
                        "PollStart": None,
                        "PollEnd": None,
                        "UserJoin": join_handler,
                        "UserLeave": leave_handler,
                        "DeleteMessage": None
                    }

                    switch[msg["event"]](self, msg["data"])

            except KeyError as e:
                self.logger.error(e)
                pass
