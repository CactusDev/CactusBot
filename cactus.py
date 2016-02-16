# CactusBot!

from user import User
from json import load


class Cactus(User):
    def __init__(self, debug=False):
        super(Cactus, self).__init__()
        self.debug = debug

    def load_config(self, filename="config.json"):
        with open(filename) as config:
            self.channel_data = self.login(**load(config))
            self.username = self.channel_data['username']

    def run(self):
        self.load_config()
        print("Authenticated as: {user}".format(user=self.username))

cactus = Cactus()
cactus.run()
