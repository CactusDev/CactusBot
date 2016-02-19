# CactusBot!

from user import User
from json import load
from traceback import format_exc
from time import sleep
from os.path import exists
from shutil import copyfile


class Cactus(User):
    starts = 0

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
                auth = {n: self.config[n] for n in ('username', 'password')}
                self.channel_data = self.login(**auth)
                self.username = self.channel_data['username']
        else:
            self.logger.warn("Config file was not found. Creating...")
            copyfile("data/config-template.json", filename)
            self.logger.info(
                "Config created. Please enter information, and restart.")
            raise FileNotFoundError("Config not found.")

    def run(self, *args, **kwargs):
        """Run bot."""

        while self.autorestart or not self.starts:
            try:
                self._run(*args, **kwargs)
            except KeyboardInterrupt:
                self.logger.info("Removing thorns... done.")
                self.logger.info("CactusBot deactivated.")
                self.autorestart = False
            except Exception:
                self.logger.critical("Oh no, I crashed!")
                self.logger.error('\n\n' + format_exc())

                if self.autorestart:
                    self.logger.info("Restarting in 10 seconds...")
                    try:
                        sleep(10)
                    except KeyboardInterrupt:
                        self.logger.info("CactusBot deactivated.")
                        self.autorestart = False

    def _run(self, config_file="data/config.json"):
        """Bot execution code."""
        self.starts += 1

        self.load_config(filename=config_file)
        self.logger.info("Authenticated as: {}.".format(self.username))

        channel = self.get_channel(self.config['channel'])
        status = {True: "online", False: "offline"}[channel.get('online')]
        self.logger.info("Channel {ch} (id {id}) is {status}.".format(
            ch=channel['token'], id=channel['id'], status=status
        ))

cactus = Cactus(debug=True, autorestart=False)
cactus.run()
