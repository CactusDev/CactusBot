# CactusBot!

from user import User
from json import load
from traceback import format_exc
from time import sleep
from os.path import exists
from shutil import copyfile


class Cactus(User):
    def __init__(self, autorestart=True, **kwargs):
        super(Cactus, self).__init__(**kwargs)
        self.debug = kwargs.get('debug', False)
        self.autorestart = autorestart

    def load_config(self, filename):
        """Load configuration."""

        if exists(filename):
            self.logger.info("Config file was found. Loading...")
            with open(filename) as config:
                self.config = load(config)
                self.channel_data = self.login(**self.config)
                self.username = self.channel_data['username']
        else:
            self.logger.error("Config file was not found. Creating...")
            copyfile("data/config-template.json", filename)
            self.logger.info(
                "Config created. Please enter information, and restart.")
            raise FileNotFoundError("Config not found.")

    def run(self, config_file="data/config.json"):
        """Run bot."""
        
        try:
            self.load_config(filename=config_file)
            self.logger.info("Authenticated as: {}.".format(self.username))
        except KeyboardInterrupt:
            self.logger.info("Removing thorns... done.")
            self.logger.info("CactusBot deactivated.")
        except Exception:
            self.logger.critical("Oh no, I crashed!")
            self.logger.debug(format_exc())
            if self.autorestart:
                self.logger.info("Restarting in 10 seconds...")
                try:
                    sleep(10)
                except KeyboardInterrupt:
                    self.logger.info("CactusBot deactivated.")
                    exit()
                self.run(config_file=config_file)

cactus = Cactus(debug=True, autorestart=True)
cactus.run()
