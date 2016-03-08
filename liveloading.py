from websocket import create_connection
# from user import User
from json import loads, dumps
from re import match


class Liveloading:
    packet_id = 0

    def connect(self, username):
        print("Connecting to the live-socket")

        self.websocket = create_connection(
            "wss://realtime.beam.pro/socket.io/?EIO=3&transport=websocket")
        response = self.websocket.recv()
        print("Connected to the live-socket")

        # is_partnered = User().get_channel(
        #     username, fields="partnered")["partnered"]

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
        events = (
            "channel:2151:update",
            "user:2547:update",
            "channel:2151:followed"
        )

        for event in events:
            packet = packet_template.copy()
            packet[1]["data"]["slug"][0] = event
            self.websocket.send("420" + dumps(packet))

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
                            print("Viewer count is now {}.".format(
                                packet[1].get("viewersCurrent")))

server = Liveloading()
server.connect('2Cubed')
