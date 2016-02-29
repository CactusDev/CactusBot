# CactusBot!

from user import User
from json import load, loads, dumps
from traceback import format_exc
from time import strftime, sleep
from os.path import exists
from shutil import copyfile

import sqlite3 as sql

import asyncio


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


class Cactus(User):
    started = False
    msg_id = 0

    def __init__(self, autorestart=True, **kwargs):
        super(Cactus, self).__init__(**kwargs)
        self.debug = kwargs.get("debug", False)
        self.autorestart = autorestart
        self.config_file = kwargs.get("config_file", "data/config.json")

    def check_db(self):
        if exists("data/bot.db"):
            self.logger.info("Found database.")
        else:
            self.logger.info("Database wasn't found.")
            self.logger.info("Creating and setting defaults...")

            conn = sql.connect("data/bot.db")
            c = conn.cursor()

            c.execute("""CREATE TABLE commands
                (command text, response text,  access text)""")

            c.execute("""CREATE TABLE bot
                (joinTime text, joinDate text, different text, total text)""")

            c.execute('''CREATE TABLE points
                (username text, points integer)''')

            c.execute('''CREATE TABLE bannedWords
                (word text)''')

            c.execute("""INSERT INTO bot VALUES
                ("{time}", "{date}", "0", "0")""".format(
                time=strftime("%I-%M-%S-%Z"), date=strftime("%a-%B-%Y")
            ))

            conn.commit()
            conn.close()

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

    def run(self, *args, **kwargs):
        """Run bot."""

        self.logger.info(cactus_art)
        self.check_db()

        while self.autorestart or not self.started:
            try:
                self._run(args, kwargs)

                loop = asyncio.get_event_loop()

                loop.run_until_complete(
                    self.connect(self.channel_data['id'], self.bot_data['id'])
                )

                tasks = asyncio.gather(
                    asyncio.async(self.send_message(
                        "CactusBot activated. Enjoy! :cactus")
                    ),
                    asyncio.async(self.read_chat())
                )

                loop.run_until_complete(tasks)
            except KeyboardInterrupt:
                self.logger.info("Removing thorns... done.")
                self.logger.info("CactusBot deactivated.")
                self.autorestart = False
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
                        self.autorestart = False
                        exit()
                else:
                    self.logger.info("CactusBot deactivated.")
                    exit()

    def _run(self, *args, **kwargs):
        if self.load_config(filename=self.config_file):
            auth = {n: self.config[n] for n in ("username", "password")}
            self.bot_data = self.login(**auth)
            self.username = self.bot_data["username"]
            self.bot_id = self.bot_data["id"]
            self.logger.info("Authenticated as: {}.".format(self.username))

        """Bot execution code."""
        self.started = True

        self.channel = self.get_channel(self.config["channel"])
        self.chan_id = self.channel["id"]
        status = {True: "online", False: "offline"}[self.channel.get("online")]

        self.channel = self.config["channel"]
        self.channel_data = self.get_channel(self.channel)

        self.logger.info("Channel {ch} (id {id}) is {status}.".format(
            ch=self.channel_data["token"], id=self.channel_data["id"],
            status=["offline", "online"][self.channel_data.get("online")]
        ))


if __name__ == "__main__":
    cactus = Cactus(debug="info", autorestart=False)
    cactus.run()
