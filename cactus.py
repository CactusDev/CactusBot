# CactusBot!

from messages import MessageHandler
from user import User

from os.path import exists
from json import load
from shutil import copyfile

from asyncio import get_event_loop, gather

from traceback import format_exc
from time import sleep

from models import Base, engine


cactus_art = """CactusBot initialized!

      ,`""',
      ;' ` ;
      ;`,',;
      ;' ` ;
 ,,,  ;`,',;               _____           _
;,` ; ;' ` ;   ,',        / ____|         | |
;`,'; ;`,',;  ;,' ;      | |     __ _  ___| |_ _   _ ___
;',`; ;` ' ; ;`'`';      | |    / _` |/ __| __| | | / __|
;` '',''` `,',`',;       | |___| (_| | (__| |_| |_| \__ \\
 `''`'; ', ;`'`'          \_____\__,_|\___|\__|\__,_|___/
      ;' `';
      ;` ' ;
      ;' `';
      ;` ' ;
      ; ',';
      ;,' ';

Made by: 2Cubed, Innectic, and ParadigmShift3d
"""


class Cactus(MessageHandler, User):
    started = False
    message_id = 0

    def __init__(self, autorestart=True, **kwargs):
        super(Cactus, self).__init__(**kwargs)
        self.debug = kwargs.get("DEBUG", False)
        self.autorestart = autorestart
        self.config_file = kwargs.get("config_file", "data/config.json")
        self.database = kwargs.get("database", "data/data.db")

    def check_db(self):
        """Ensure the database exists."""

        if exists(self.database):
            self.logger.info("Found database.")
        else:
            self.logger.info("Database wasn't found.")
            self.logger.info("Creating and setting defaults...")

            Base.metadata.create_all(engine)

            self.logger.info("Done!")

    def load_config(self, filename):
        """Load configuration."""

        if exists(filename):
            self.logger.info("Config file was found. Loading...")
            with open(filename) as config:
                self.config = load(config)
                return True
        else:
            self.logger.warn("Config file was not found. Creating...")
            copyfile("data/config-template.json", filename)
            self.logger.error(
                "Config created. Please enter information, and restart.")
            raise FileNotFoundError("Config not found.")

    def load_stats(self):
        if exists('data/stats.json'):
            self.logger.info("Config file was found. Loading...")
            with open('data/stats.json') as config:
                self.config = load(config)
                return True
        else:
            self.logger.warn("Config file was not found. Creating...")
            copyfile("data/stats-templace.json", 'data/stats.json')
            self.logger.error(
                "Config created. Please enter information, and restart.")
            raise FileNotFoundError("Config not found.")

    def run(self, *args, **kwargs):
        """Run bot."""

        self.logger.info(cactus_art)
        self.check_db()

        while self.autorestart or not self.started:
            try:
                self._run(args, kwargs)

                loop = get_event_loop()

                self.connected = bool(loop.run_until_complete(
                    self.connect(self.channel_data['id'], self.bot_data['id'])
                ))

                self.logger.info("{}uccessfully connected to chat {}.".format(
                    ['Uns', 'S'][self.connected], self.channel_data["token"]
                ))

                if self.connected:
                    tasks = gather(
                        self.send_message(
                            "@{}: CactusBot activated. Enjoy! :cactus".format(
                              self.channel_data["token"]
                            )
                        ),
                        self.read_chat(self.handle),
                    )

                    loop.run_until_complete(tasks)
                else:
                    raise ConnectionError
            except KeyboardInterrupt:
                self.logger.info("Removing thorns... done.")
                if self.connected:
                    loop.run_until_complete(
                        self.send_message("CactusBot deactivated! :cactus")
                    )
                    pass
                self.logger.info("CactusBot deactivated.")
                exit()
            except Exception:
                self.logger.critical("Oh no, I crashed!")
                self.logger.error("\n\n" + format_exc())

                if self.autorestart:
                    self.logger.info("Restarting in 10 seconds...")
                    try:
                        sleep(10)
                    except KeyboardInterrupt:
                        self.logger.info("CactusBot deactivated.")
                        exit()
                else:
                    self.logger.info("CactusBot deactivated.")
                    exit()

    def _run(self, *args, **kwargs):
        """Bot execution code."""

        if self.load_config(filename=self.config_file):
            auth = {n: self.config[n] for n in ("username", "password")}
            self.bot_data = self.login(**auth)
            self.username = self.bot_data["username"]
            self.bot_id = self.bot_data["id"]
            self.logger.info("Authenticated as: {}.".format(self.username))

        self.started = True

        self.channel = self.config["channel"]
        self.channel_data = self.get_channel(self.channel)

        self.logger.info("Channel {ch} (id {id}) is {status}.".format(
            ch=self.channel_data["token"], id=self.channel_data["id"],
            status=["offline", "online"][self.channel_data["online"]]
        ))

        # print(self.channel)

if __name__ == "__main__":
    cactus = Cactus(debug="debug", autorestart=False)
    cactus.run()
