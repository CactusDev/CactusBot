from logging import getLogger as get_logger
from logging import WARNING
from requests import Session
from json import dumps, loads
from websockets import connect


class User:
    path = "https://beam.pro/api/v1"

    def __init__(self, debug="WARNING", **kwargs):
        self._init_logger(debug)
        print(self.authKey())

    def _init_logger(self, level):
        """Initialize logger."""

        self.logger = get_logger('CactusBot')

        level = level.upper()

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
                    params=kwargs.get("params")
                )
            else:
                response = self.session.__getattribute__(req.lower())(
                    self.path + url,
                    data=kwargs.get("data")
                )

            if 'error' in response.json().keys():
                self.logger.warn("Error: {}".format(response.json()['error']))

            return response.json()
        else:
            self.logger.debug("Invalid request: {}".format(req))

    def authKey(self):
        """Get the required authKey from Beam"""
        return self.request("GET", "/chats/join")

    def login(self, username, password, code=''):
        """Authenticate and login with Beam."""
        return self.request("GET", "/users/login", locals())

    def get_channel(self, id, **p):
        """Get channel data by username."""
        channel = self.request("GET", "/channels/{id}".format(id=id))
        return channel

    def send_chat(self, id, message):
        """
        Send a message for a certain chat
        Arguments:
        - id: Channel ID to send message to
        - message: Chat message to send
        """
        # Packet to send to Beam
        # packet = {t pu}


class Chatter:

    def ban(username):
        pass

    def purge(username):
        pass

    def timeout(username, time):
        pass
