from requests import Session
from logging import getLogger


class User:
    path = path = "https://beam.pro/api/v1"

    def __init__(self, debug="WARNING", **kwargs):
        self.session = Session()
        self._init_logger(debug)

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

    def login(self, username, password, code=''):
        """Authenticate and login with Beam."""
        auth = {
            "username": username,
            "password": password,
            "code": code
        }

        channel_data = self.request("POST", "/users/login", auth)

        return channel_data

    def get_channel(self, username):
        """Get channel data by username."""
        user_json = self.request('get', "/channels/{user}".format(
            user=username)
        ).json()
        return user_json.get('id')
