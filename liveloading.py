from websocket import create_connection
from socketIO_client import SocketIO, LoggingNamespace


from user import User
import logging
from json import load, loads, dump, dumps
from re import match


class Server:
    packet_id = 0

    def __init__(self):
        logging.getLogger('requests').setLevel(logging.WARNING)
        logging.basicConfig(level=logging.DEBUG)

    def connect(self, username):
        print("Connecting to the live-socket")

        print("Connected to the live-socket")

        self.websocket = SocketIO('realtime.beam.pro', 8000, LoggingNamespace)
        # self.websocket.wait(seconds=1)
        response = self.websocket.recv()

        is_partnered = User().get_channel(username, fields="partnered")["partnered"]

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

        # Subscribing to channel events
        packet = packet_template.copy()
        packet[1]["data"]["slug"][0] = "channel:2151:update"
        self.websocket.send('42' + str(self.packet_id) + dumps(packet))

        # Subscribing to user events
        packet = packet_template.copy()
        packet[1]["data"]["slug"][0] = "user:2547:update"
        self.websocket.send('42' + str(self.packet_id) + dumps(packet))

        # Subscribe to folloself.websocket
        packet = packet_template.copy()
        packet[1]["data"]["slug"][0] = "channel:2151:followed"
        self.websocket.send('42' + str(self.packet_id) + dumps(packet))

        self.packet_id += 1
        response = self.websocket.recv()

        assert response.startswith("40")
        self.websocket.send("2")
        response = self.websocket.recv()

        assert response.startswith("42")
        print("Connected to the live-socket")

        while True:
            response = self.websocket.recv()
            print(response)
            packet = match('\d+(.+)?', response)
            if packet:
                if packet.group(1):
                    packet = loads(packet.group(1))
                    if isinstance(packet[0], str):
                        if packet[1].get("viewersCurrent"):
                            print("Viewer count is now {}.".format(packet[1].get("viewersCurrent")))
            print("DONE")
            # if "viewersCurrent" in recv:
            #     self.total_index += 1
            #     recv = recv[2:]
            #     data = loads(recv)
            #     curr = data[1]['viewersCurrent']
            #     self.total_viewer += curr
            # elif "viewersTotal" in recv:
            #     recv = recv[2:]
            #     data = loads(recv)
            #     curr = data[1]['viewersTotal']
            #
            #     self.total_viewed = curr
            # elif "followed" in recv:
            #     recv = recv[2:]
            #     data = loads(recv)
            #     is_following = (data[1]['following'])
            #
            #     if is_following is True:
            #         self.total_followers += 1
            #     else:
            #         self.total_unfollowers += 1
                # average = self.total_viewer / self.total_index
                #
                # with open('data/stats.json', 'r+') as f:
                #     stats = load(f)
                #
                #     stats['average-viewers'] = average
                #     stats['total-vieself.websocket'] = curr
                #
                #     curr_followers = stats['total-followers']
                #     stats['total-followers'] = (self.total_followers + int(curr_followers))
                #
                #     curr_unfollows = stats['total-unfollows']
                #     stats['total-unfolows'] = (self.total_unfollows + int(curr_unfollows))
                #
                #     dump(stats, f, indent=4, sort_keys=True)

server = Server()
server.connect('2Cubed')
