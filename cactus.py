# CactusBot!

from user import User
from json import load, loads, dumps
from traceback import format_exc
from time import strftime, sleep
from os.path import exists
from shutil import copyfile

import sqlite3 as sql
import asyncio
import websockets


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

    def __init__(self, autorestart=True, **kwargs):
        super(Cactus, self).__init__(**kwargs)
        self.starts = False
        self.msg_id = 0
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

        while True:
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

            packet = self.msg_packet
            packet["id"] = self.msg_id
            packet["arguments"] = ["MUAHAHA! I AM ALIVE! :mappa <3 :cactus"]

            yield from self.send_message(dumps(packet))
            ret = yield from self.websocket.recv()
            self.logger.info(result)

            if result is None:
                continue
            try:
                result = loads(result)
            except TypeError:
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

            c.execute("""INSERT INTO bot VALUES("{time}, {date}, "\0", "\0"")""".format(
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

        while self.autorestart or not self.starts:
            try:
                self._run(args, kwargs)
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

    def _run(self, *args, **kwargs):
        if self.load_config(filename=self.config_file):
            auth = {n: self.config[n] for n in ("username", "password")}
            self.channel_data = self.login(**auth)
            self.username = self.channel_data["username"]
            self.logger.info("Authenticated as: {}.".format(self.username))

        """Bot execution code."""
        self.starts = True

        success = self.load_config(filename=self.config_file)
        if success:
            auth = {n: self.config[n] for n in ("username", "password")}
            self.channel_data = self.login(**auth)
            self.username = self.channel_data["username"]
            self.bot_id = self.channel_data["id"]
            self.logger.info("Authenticated as: {}.".format(self.username))

        self.channel = self.get_channel(self.config["channel"])
        self.chan_id = self.channel["id"]
        status = {True: "online", False: "offline"}[self.channel.get("online")]

        self.logger.info("Channel {ch} (id {id}) is {status}.".format(
            ch=self.channel["token"], id=self.channel["id"], status=status
        ))

        loop = asyncio.get_event_loop()

        tasks = [
            asyncio.async(self.read_chat(self.chan_id))
        ]

        try:
            loop.run_until_complete(asyncio.wait(tasks))
        except Exception as e:
            self.logger.error("An error has occurred.")
            self.logger.error(e)
            loop.close()

if __name__ == "__main__":
    cactus = Cactus(debug=True, autorestart=False)
    cactus.run()
