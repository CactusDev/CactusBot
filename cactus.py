# CactusBot!

from user import User
from json import load
from traceback import format_exc
from time import sleep
from os.path import exists
from shutil import copyfile
from time import strftime
from utils import get_server
from utils import get_id
from utils import get_authkey

import sqlite3 as sql
import asyncio
import websockets
import json


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
    starts = 0

    def __init__(self, autorestart=True, **kwargs):
        super(Cactus, self).__init__(**kwargs)
        self.debug = kwargs.get("debug", False)
        self.autorestart = autorestart

    @asyncio.coroutine
    def read_chat(self, user, bot):
        buid = get_id(self, bot)
        uid = get_id(self, user)
        server = get_server(self, uid)
        auth = get_authkey(self, uid)

        print("Connecting to: {server}".format(server=server))
        print("Connecting with authkey: {auth}".format(auth=auth))

        while True:
            websocket = yield from websockets.connect(server)  # Need to get the server to connect to
            websocket.send('''{"type":"method","method":"auth","arguments":[{chanId},{botid},"{auth}"],"id":1}'''.format(chanId=uid, botid=buid, auth=auth))
            print(websocket.recv())
            websocket.send('''{"type":"method","method":"msg","arguments":["Hello World!"],"id":2}''')
            print(websocket.recv())

            result = yield from websocket.recv()

            if result is None:
                continue
            try:
                result = json.loads(result)
            except TypeError as e:
                print(e)

                continue

            if 'event' in result:
                event = result['event']

                if 'username' in result['data']:
                    user = result['data']['username']
                elif 'user_name' in result['data']:
                    user = result['data']['user_name']

                if event == "UserJoin":
                    print(event)
                elif event == "UserLeave":
                    # Apply to statistics
                    pass
                elif event == "ChatMessage":
                    print(event)

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

            c.execute("""INSERT INTO bot VALUES("{time}, {date}, "\0", "\0"")""".format(time=strftime("%I-%M-%S-%Z"), date=strftime("%a-%B-%Y")))

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
                self._run(*args, **kwargs)
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

        loop = asyncio.get_event_loop()

        tasks = [
            asyncio.async(self.read_chat("innectic", "innectbot"))
        ]

        try:
            loop.run_until_complete(asyncio.wait(tasks))
        except Exception as e:
            print("An error has occurred.")
            print(e)
            loop.close()

    def _run(self, config_file="data/config.json"):
        """Bot execution code."""
        self.starts += 1

        self.load_config(filename=config_file)
        self.logger.info("Authenticated as: {}.".format(self.username))

        channel = self.get_channel(self.config["channel"])
        status = {True: "online", False: "offline"}[channel.get("online")]
        self.logger.info("Channel {ch} (id {id}) is {status}.".format(
            ch=channel["token"], id=channel["id"], status=status
        ))

cactus = Cactus(debug="info", autorestart=False)
cactus.run()
