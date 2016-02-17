# CactusBot!

from user import User
from json import load

import logging


class Cactus(User):
    def __init__(self, debug=False):
        super(Cactus, self).__init__()
        self.debug = debug

    def load_config(self, filename="config.json"):
        with open(filename) as config:
            self.config = load(config)
            self.channel_data = self.login(**self.config)
            self.username = self.channel_data['username']

            self.login(self.username, self.config['password'])

    def run(self):
        self.load_config()
        logging.info("Authenticated as: {user}.".format(user=self.username))

cactus = Cactus()
cactus.run()
