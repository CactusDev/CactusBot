from logging import getLogger as get_logger
from logging import WARNING
from requests import Session
from json import dumps, loads
from websockets import connect


class User:
    path = "https://beam.pro/api/v1"

    def __init__(self, debug="WARNING", **kwargs):
        self._init_logger(debug)
        self.session = Session()

    def _init_logger(self, level):
        """Initialize logger."""

        self.logger = get_logger('CactusBot')

        if level is True:
            level = "DEBUG"
        elif level is False:
            level = "WARNING"

        levels = ("CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "NOTSET")
        if level in levels:
            level_num = __import__("logging").__getattribute__(level)
            self.logger.setLevel(level_num)
            get_logger("urllib3").setLevel(WARNING)
            get_logger("websockets").setLevel(WARNING)
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

    def connect(self, channel_id, bot_id):
        """Connect to a Beam chat through a websocket."""

        chat = self.get_chat(channel_id)
        server = chat["endpoints"][0]
        authkey = chat["authkey"]

        self.logger.debug("Connecting to: {server}".format(server=server))

        self.websocket = yield from connect(server)

        response = yield from self.send_message(
            (channel_id, bot_id, authkey), method="auth"
        )

        response = loads(response)

        if response["data"]["authenticated"]:
            self.logger.debug(response)
            return self.websocket
        return False

    def send_message(self, arguments, method="msg"):
        """Send a message to a Beam chat through a websocket."""

        if isinstance(arguments, str):
            arguments = (arguments,)

        msg_packet = {
            "type": "method",
            "method": method,
            "arguments": arguments,
            "id": self.message_id
        }

        yield from self.websocket.send(dumps(msg_packet))
        self.message_id += 1

        return (yield from self.websocket.recv())

    def remove_message(self, channel_id, message_id):
        """Remove a message from chat."""
        return self.request("DELETE", "/chats/{id}/message/{message}".format(
            id=channel_id, message=message_id))

    def read_chat(self, handle=None):
        while True:
            response = loads((yield from self.websocket.recv()))
            self.logger.debug(response)

            if handle:
                handle(response)

    def get_channel_name(self, id):
        req = self.request("GET", "/channels/{id}".format(id=id))
        j = loads(req)
        return j['token']
