from logging import getLogger as get_logger
from requests import Session
import asyncio
from websockets import connect
from json import dumps, loads


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

    @asyncio.coroutine
    def send_message(self, packet):
        yield from self.websocket.send(packet)
        response = yield from self.websocket.recv()
        return response

    @asyncio.coroutine
    def read_chat(self, channel_id, bot_id):
        chat = self.get_chat(channel_id)
        server = chat["endpoints"][0]
        auth = chat["authkey"]

        self.logger.debug("Connecting to: {server}".format(server=server))

        self.msg_packet = {
            "type": "method",
            "method": "msg",
            "arguments": [],
            "id": self.msg_id
        }

        while True:
            self.websocket = yield from connect(server)

            auth_packet = {
                "type": "method",
                "method": "auth",
                "arguments": [
                    channel_id,
                    bot_id,
                    auth
                ],
                "id": self.msg_id
            }

            yield from self.send_message(dumps(auth_packet))

            result = yield from self.websocket.recv()
            print(auth_packet)
            self.logger.info(result)

            self.msg_id += 1

            packet = self.msg_packet.copy()
            packet["id"] = self.msg_id
            packet["arguments"] = ["Hello World! :cactus"]

            yield from self.send_message(dumps(packet))
            response = yield from self.websocket.recv()
            self.logger.info(response)

            if result is None:
                continue
            try:
                result = loads(result)
            except TypeError:
                continue
