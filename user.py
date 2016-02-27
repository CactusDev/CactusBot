from logging import getLogger as get_logger
from requests import Session


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

    def login(self, username, password, code=''):
        """Authenticate and login with Beam."""
        l = locals()
        packet = {n: l[n] for n in ("username", "password", "code")}
        return self.request("POST", "/users/login", packet)

    def get_channel(self, id, **p):
        """Get channel data by username."""
        return self.request("GET", "/channels/{id}".format(id=id), params=p)
        
    def get_chat(self, id, **p):
        """Get chat server data."""
        return self.request("GET", "/chats/{id}".format(id=id), params=p)
