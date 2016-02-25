from utils import request
from logging import getLogger as get_logger
from requests import Session


class User:
    path = path = "https://beam.pro/api/v1"

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

    def login(self, username, password, code=''):
        """Authenticate and login with Beam."""
        try:
            res = request("POST", "/users/login", locals())
            return res
        except Exception as e:
            print (e)
            return False

    def get_channel(self, id):
        """Get channel data by username."""
        try:
            res = return request("GET", "/channels/{id}".format(id=id))
            return res
        except Exception as e:
            print (e)
            return False
