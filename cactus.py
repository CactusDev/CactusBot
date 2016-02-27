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
        self.debug = kwargs.get("debug", False)
        self.autorestart = autorestart
        self.starts = False
        self.config_file = "data/config.json"

    @asyncio.coroutine
    def send_message(self, packet):
        yield from self.websocket.send(packet)
        ret = yield from self.websocket.recv()
        return ret

    @asyncio.coroutine
    def read_chat(self, user, bot):
        self.buid = self.get_channel(bot, fields="id")["id"]
        self.uid = self.get_channel(user, fields="id")["id"]
        self.chat = self.get_chat(uid)
        self.server = self.chat["endpoints"][0]
        self.auth = self.chat["authkey"]

        self.logger.debug("Connecting to: {server}".format(server=self.server))

        # Packet Templates
        # Message packet
        self.message_packet = {
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
                    self.uid,
                    self.buid,
                    self.auth
                ],
                "id": 1
            }

            yield from self.send_message(dumps(auth_packet))
            print(websocket.recv())
            websocket.send(dumps(msg_packet))
            print(websocket.recv())

            result = yield from websocket.recv()

            # Increment msg ID
            self.msg_id += 1

            yield from self.send_message(auth_packet)
            ret = yield from self.websocket.recv()
            yield from self.send_message(message_packet)

            result = yield from self.websocket.recv()

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
                auth = {n: self.config[n] for n in ("username", "password")}
                self.channel_data = self.login(**auth)
                self.username = self.channel_data["username"]
                self.channel = self.config["channel"]

                # Successful
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

        loop = asyncio.get_event_loop()

        tasks = [
            asyncio.async(self.read_chat(self.channel, self.username))
        ]

        """Bot execution code."""
        self.starts = True

        success = self.load_config(filename=self.config_file)
        if success:
            auth = {n: self.config[n] for n in ("username", "password")}
            self.channel_data = self.login(**auth)
            self.username = self.channel_data["username"]
            self.logger.info("Authenticated as: {}.".format(self.username))

        channel = self.get_channel(self.config["channel"])
        status = {True: "online", False: "offline"}[channel.get("online")]
        self.logger.info("Channel {ch} (id {id}) is {status}.".format(
            ch=channel["token"], id=channel["id"], status=status
        ))

        try:
            loop.run_until_complete(asyncio.wait(tasks))
        except Exception as e:
            print("An error has occurred.")
            print(e)
            loop.close()

cactus = Cactus(debug="info", autorestart=False)

cactus = Cactus(debug=True, autorestart=False)
cactus.run()
