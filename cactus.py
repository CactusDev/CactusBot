# CactusBot!

from user import User
from json import load
from traceback import format_exc
from time import strftime, sleep
from os.path import exists
from shutil import copyfile
from chat import Chat

import sqlite3 as sql

import asyncio


cactus_art = """CactusBot initialized!

      ,`""',
      ;' ` ;
      ;`,',;
      ;' ` ;
 ,,,  ;`,',;
;,` ; ;' ` ;   ,',
;`,'; ;`,',;  ;,' ;       ------ /------\  ------ --------  |       |    -----
;',`; ;` ' ; ;`'`';       |      |      |  |         |      |       |   \\
;` '',''` `,',`',;        |      |      |  |         |      |       |    ----\\
 `''`'; ', ;`'`'          |      |------|  |         |      |       |        |
      ;' `';              ------ |      |  ------    |      ---------   -----/
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

            c.execute('''CREATE TABLE bannedWords
                (word text)''')

            c.execute("""INSERT INTO bot VALUES("{time}", "{date}", "0", "0")""".format(
                time=strftime("%I-%M-%S-%Z"), date=strftime("%a-%B-%Y")))

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
            self.logger.info(
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

                tasks = asyncio.gather(
                    asyncio.async(self.read_chat(
                        self.channel_data['id'],
                        self.bot_data['id']
                    ))
                )

                loop.run_until_complete(tasks)
            except KeyboardInterrupt:
                self.logger.info("Removing thorns... done.")
                self.logger.info("CactusBot deactivated.")
                self.autorestart = False
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
                else:
                    self.logger.info("CactusBot deactivated.")
                    exit()
            finally:
                loop.close()

    def _run(self, *args, **kwargs):
        """Bot execution code."""

        self.started = True

        self.load_config(filename=self.config_file)

        auth = {n: self.config[n] for n in ("username", "password")}
        self.bot_data = self.login(**auth)
        self.username = self.bot_data["username"]
        self.logger.info("Authenticated as: {}.".format(self.username))

        self.channel = self.config["channel"]
        self.channel_data = self.get_channel(self.channel)

        self.logger.info("Channel {ch} (id {id}) is {status}.".format(
            ch=self.channel_data["token"], id=self.channel_data["id"],
            status=["offline", "online"][self.channel_data.get("online")]
        ))


if __name__ == "__main__":
    cactus = Cactus(debug=True, autorestart=False)
    cactus.run()
