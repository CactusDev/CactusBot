# CactusBot!

from user import User
from json import load
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

    @asyncio.coroutine
    def send_message(self, packet):
        yield from self.websocket.send(packet)
        ret = yield from self.websocket.recv()
        return ret

    @asyncio.coroutine
    def read_chat(self, chan):
        self.chan_id = self.get_channel(chan, fields="id")["id"]
        self.chat = self.get_chat(self.chan_id)
        self.server = self.chat["endpoints"][0]
        self.auth = self.chat["authkey"]

        self.logger.debug("Connecting to: {server}".format(server=self.server))

        # Packet Templates
        # Message packet
        self.msg_packet = {
            "type": "method",
            "method": "msg",
            "arguments": [],
            "id": self.msg_id
        }

        # Need to get the server to connect to
        self.websocket = yield from websockets.connect(self.server)

        auth_packet = {
            "type": "method",
            "method": "auth",
            "arguments": [
                self.chan_id,
                self.bot_id,
                self.auth
            ],
            "id": self.msg_id
        }

        yield from self.send_message(dumps(auth_packet))

        result = yield from self.websocket.recv()
        self.logger.info(result)

        # Increment msg ID
        self.msg_id += 1

        while True:
            packet = self.msg_packet
            packet["id"] = self.msg_id
            packet["arguments"] = ":mappa <3 :cactus"


            yield from self.send_message(dumps(packet))
            ret = yield from self.websocket.recv()
            self.logger.info(result)

            self.msg_id += 1

            if result is None:
                continue
            try:
                result = loads(result)
            except TypeError as e:
                self.logger.warning("Something borked in regards to JSON from Beam")
                self.logger.warning(e)
                continue

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
            self.channel_data = self.login(**auth)
            print (self.channel_data)
            self.username = self.channel_data["username"]
            self.bot_id = self.channel_data["id"]
            self.logger.info("Authenticated as: {}.".format(self.username))

        """Bot execution code."""
        self.started = True

        self.channel = self.get_channel(self.config["channel"])
        self.chan_id = self.channel["id"]
        status = {True: "online", False: "offline"}[self.channel.get("online")]

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
    cactus = Cactus(debug="info", autorestart=False)
    cactus.run()
