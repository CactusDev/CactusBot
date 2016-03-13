# CactusBot!

from messages import MessageHandler
from user import User
from models import Base, engine
from schedule import Scheduler

from beam import Beam

from os.path import exists
from time import sleep
from json import load, dump
from shutil import copyfile
from functools import reduce

from asyncio import get_event_loop, gather, async

from traceback import format_exc

import argparse


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


class Cactus(MessageHandler, Beam):
    started = False
    connected = False
    message_id = 0

    def __init__(self, verbose=False, silent=False, nm=False, autorestart=True, **kwargs):
        super(Cactus, self).__init__(**kwargs)
        self.debug = kwargs.get("DEBUG", False)
        self.autorestart = autorestart
        self.config_file = kwargs.get("config_file", "data/config.json")
        self.stats_file = kwargs.get("stats_file", "data/stats.json")
        self.database = kwargs.get("database", "data/data.db")
        self.verbose = verbose
        self.silent = silent
        self.no_messages = nm

    def _init_database(self, database):
        """Ensure the database exists."""

        if exists(database):
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
                return self.config
        else:
            self.logger.warn("Config file was not found. Creating...")
            copyfile("data/config-template.json", filename)
            self.logger.error(
                "Config file created. Please enter values and restart.")
            raise FileNotFoundError("Config not found.")
        self.config_file = filename

    def load_stats(self, filename):
        if exists(filename):
            self.logger.info("Stats file was found. Loading...")
            with open(filename) as stats:
                self.stats = load(stats)
                return self.stats
        else:
            self.logger.warn("Statistics file was not found. Creating...")
            copyfile("data/stats-templace.json", "data/stats.json")
            self.logger.error(
                "Statistics file created. Please enter values and restart.")
            raise FileNotFoundError("Statistics file not found.")
        self.stats_file = filename

    def update_config(self, keys, value):
        with open(self.config_file, 'r') as config:
            config_data = load(config)
            reduce(lambda d, k: d[k], keys.split('.')[:-1], config_data)[
                keys.split('.')[-1]] = value
        with open(self.config_file, 'w+') as config:
            dump(config_data, config, indent=4, sort_keys=True)
        self.config = config_data

    def update_stats(self, keys, value):
        with open(self.stats_file, 'r') as stats:
            stats_data = load(stats)
            reduce(lambda d, k: d[k], keys.split('.')[:-1], stats_data)[
                keys.split('.')[-1]] = value
        with open(self.config_file, 'w+') as config:
            dump(stats_data, config, indent=4, sort_keys=True)
        self.config = stats_data

    def run(self, *args, **kwargs):
        """Run bot."""

        self.logger.info(cactus_art)
        self._init_database(self.database)

        while self.autorestart or not self.started:
            try:
                self._run(args, kwargs)

                self.loop = get_event_loop()

                self.init_scheduler()

                self.connected = bool(loop.run_until_complete(
                    self.connect(self.channel_data["id"], self.bot_data["id"])
                ))

                self.logger.info("{}uccessfully connected to chat {}.".format(
                    ['Uns', 'S'][self.connected], self.channel_data["token"]
                ))

                if not self.no_messages:
                    self.loop.run_until_complete(self.send_message(
                        "CactusBot activated. Enjoy! :cactus")
                    )

                if self.connected:
                    tasks = gather(
                        async(self.read_chat(self.handle))
                    )

                    self.loop.run_until_complete(tasks)
                else:
                    raise ConnectionError
            except KeyboardInterrupt:
                self.logger.info("Removing thorns...")
                self.logger.info("CactusBot deactivated.")
                if self.connected and not self.no_messages:
                    self.loop.run_until_complete(
                        self.send_message("CactusBot deactivated! :cactus")
                    )
                    pass
                else:
                    pass

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
            self.bot_data = self.login(**self.config["auth"])
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


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s",
        "--silent",
        dest="silent",
        help="Run the bot silently (no messages sent to chat)",
        action="store_true",
        default=False
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Run the bot with verbose debug output",
        default=False
    )
    parser.add_argument(
        "-nm",
        action="store_true",
        help="Run the bot without the startup/quit messages",
        default=False
    )
    parser.add_argument(
        "--autorestart",
        action="store_true",
        help="Have the bot automatically restart on crash",
        default=False
    )

    parsed = parser.parse_args()

    cactus = Cactus(
        debug="info",
        autorestart=parsed.autorestart,
        silent=parsed.silent,
        verbose=parsed.verbose,
        nm=parsed.nm
    )
    cactus.run()
