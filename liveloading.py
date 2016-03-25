from websockets import connect
from json import loads, dumps, load, dump
from re import match
from time import time
from threading import Thread
from beam import Beam
from functools import reduce


class Liveloading:
    last_ping = 0

    follows = 0
    unfollows = 0
    subs = 0
    resubs = 0

    view_index = 0
    viewers = 0
    views = 0

    commands_run = 0
    deleted_messages = 0
    total_messages = 0

    usr = Beam()

    def add_run_command(self):
        self.commands_run += 1

    def add_deleted(self):
        self.deleted_messages += 1

    def add_message(self):
        self.total_messages += 1

    def add_view(self):
        self.views += 1

    def update_stats(self, keys, value):
        with open(self.stats_file, "r") as stats:
            stats_data = load(stats)
            reduce(lambda d, k: d[k], keys.split(".")[:-1], stats_data)[
                keys.split(".")[-1]] = value
        with open(self.config_file, "w+") as config:
            dump(stats_data, config, indent=4, sort_keys=True)
        self.config = stats_data

    def get_stat(self, loc):
        with open(self.stats_file, "r") as conf:
            conf = load(conf)

            return conf[loc]

    def parse_packet(self, packet):
        return match('\d+(.+)?', packet).group(1)

    def live_connect(self, username):
        self.logger.info("Connecting to the live-socket")

        self.websocket = yield from connect(
            "wss://realtime.beam.pro/socket.io/?EIO=3&transport=websocket")

        response = yield from self.websocket.recv()

        self.interval = int(loads(self.parse_packet(response))["pingInterval"])
        self.last_ping = time()
        self.logger.info("Connected to the live-socket")

        cid = self.usr.get_channel(username, fields=id)['id']
        uid = self.usr.get_user(username)

        packet_template = [
            "put",
            {
                "method": "put",
                "headers": {},
                "data": {
                    "slug": [
                        "channel:2151:update"
                    ]
                },
                "url": "/api/v1/live"
            }
        ]

        assert response.startswith("0")

        events = (
            "channel:{cid}:update".format(cid=cid),
            "channel:{cid}:followed".format(cid=cid),
            "channel:{cid}:subscribed".format(cid=cid),
            "channel:{cid}:resubscribed".format(cid=cid),
            "user:{uid}:update".format(uid=uid)
        )

        for event in events:
            packet = packet_template.copy()
            packet[1]["data"]["slug"][0] = event
            yield from self.websocket.send("420" + dumps(packet))

        response = yield from self.websocket.recv()
        assert response.startswith("40")
        yield from self.websocket.send("2")
        response = yield from self.websocket.recv()

        assert response.startswith("42")
        self.logger.info("Connected to the livesocket!")

        yield from self.websocket.send("42")

        def ping_again():
            while True:
                if time() - self.last_ping > 10:
                    self.last_ping = time()
                    self.websocket.send("2")
                    self.logger.debug("PING!")
                Thread(target=ping_again).start()
        try:
            while True:
                ping_again()
                response = yield from self.websocket.recv()
                packet = match('\d+(.+)?', response)
                if packet:
                    self.websocket.send("2")
                    if packet.group(1):
                        packet = loads(packet.group(1))
                        if isinstance(packet[0], str):
                            if packet[1].get("viewersCurrent"):
                                self.view_index += 1
                                self.viewers += packet[1].get('viewersCurrent')
                            elif packet[1].get('subscribed'):
                                self.subs += 1
                                username = packet[1]['user']['username']
                                yield from self.send_message(
                                    "{} just subscribed to the channel!")
                            elif packet[1].get("resubscribed"):
                                username = packet[1]
                                self.resubs += 1
                            elif packet[1].get("followed"):
                                username = packet[1]

                                if packet[1]['following'] is True:
                                    self.follows += 1

                                    yield from self.send_message(
                                        "{} just followed the channel!".format(username))
        except:
            if self.view_index is 0:
                self.logger.error("Not enough samples for average viewers!")
            else:
                average = self.viewers / self.view_index
                cur_views = self.get_stat("total-views")
                cur_commands = self.get_stat("commands-run")
                cur_subs = self.get_stat("total-subs")
                cur_resubs = self.get_stat("total-resubs")
                cur_follows = self.get_stat("total-subs")
                cur_unfollows = self.get_stat("total-unfollows")
                cur_deleted = self.get_stat("total-deleted")
                cur_messages = self.get_stat("total-messages")

                self.update_stats("average-viewers",
                                  average)

                self.update_stats("total-followers",
                                  self.follows + cur_follows)

                self.update_stats("total-unfollows",
                                  self.unfollows + cur_unfollows)

                self.update_stats("total-subs",
                                  self.subs + cur_subs)

                self.update_stats("total-resubs",
                                  self.resubs + cur_resubs)

                self.update_stats("total-views",
                                  self.views + cur_views)

                self.update_stats("commands-run",
                                  self.commands_run + cur_commands)

                self.update_stats("total-messages",
                                  self.total_messages + cur_messages)

                self.update_stats("deleted-messages",
                                  self.deleted_messages + cur_deleted)
