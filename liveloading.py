from websockets import connect
from json import loads, dumps
from re import match
from time import time
from threading import Thread
from user import User
# from messages import MessageHandler as mh
# from statistics import Statistics


class Liveloading:
    last_ping = 0

    follows = 0
    unfollows = 0
    subs = 0
    resubs = 0

    view_index = 0
    viewers = 0

    usr = User()

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
            "usr:{uid}:update".format(uid=uid)
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
            print(time())
            print(time() - self.last_ping)
            while True:
                if time() - self.last_ping > 10:
                    self.last_ping = time()
                    self.websocket.send("2")
                    self.logger.debug("PING!")
                Thread(target=ping_again).start()
        try:
            while True:
                # ping_again()
                response = yield from self.websocket.recv()
                packet = match('\d+(.+)?', response)
                if packet:
                    self.websocket.send("2")
                    if packet.group(1):
                        packet = loads(packet.group(1))
                        if isinstance(packet[0], str):
                            if packet[1].get("viewersCurrent"):
                                print("Viewer count is now {}.".format(
                                    packet[1].get("viewersCurrent")))
                            elif packet[1].get("numFollowers"):
                                print("Follower count is now {}.".format(
                                    packet[1].get("numFollowers")))
                            elif packet[1].get('subscribed'):
                                username = packet[1]['user']['username']
                                yield from self.send_message(
                                    "{} just subscribed to the channel!")
                            elif packet[1].get("resubscribed"):
                                username = packet[1]
                            elif packet[1].get("followed"):
                                username = packet[1]

                                if packet[1]['following'] is True:
                                    yield from self.send_message(
                                        "{} just followed the channel!".format(username))
        except:
            if self.view_index is 0:
                print("Not enough samples!")
            else:
                average = self.viewers / self.view_index

            # data = {
            #     "location": "live",
            #
            #     "Subs": self.subs,
            #     "Resubs": self.resubs,
            #     "Follows": self.followers,
            #     "Unfollows": self.unfollowers,
            #     "AverageViewers": average
            # }

            # Statistics.recv(data)
            # Statistics.recv(mh.get_data())

    def parse_packet(self, packet):
        return match('\d+(.+)?', packet).group(1)

# server = Liveloading()
# loop = get_event_loop()
# loop.run_until_complete(gather(server.connect("innectic")))
