from requests import Session
from logging import getLogger


class User:
    path = path = "https://beam.pro/api/v1"

    def __init__(self, debug="WARNING", **kwargs):
        self.session = Session()
        self._init_logger(debug)
        print(self.authKey())

    def _init_logger(self, level):
        """Initialize logger."""
        self.logger = getLogger('CactusBot')
        if level is True:
            level = "DEBUG"
        elif level is False:
            level = "WARNING"
        levels = ("CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "NOTSET")
        if level in levels:
            level_num = __import__("logging").__getattribute__(level)
            self.logger.setLevel(level_num)
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

    def request(self, req, url, *args, **kwargs):
        """Send HTTP request to Beam."""
        if req.lower() in ('get', 'head', 'post', 'put', 'delete', 'options'):
            response = self.session.__getattribute__(req.lower())(
                self.path + url, *args, **kwargs
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

    def get_channel(self, id):
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
