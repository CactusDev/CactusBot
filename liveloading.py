
from websocket import create_connection
from user import User
import logging
from time import sleep
from json import loads, load, dump


class Server:

    pid = 0
    packet_recv = ""
    packet_send = ""
    status = 0

    total_viewer = 0
    total_index = 0
    total_viewed = 0

    total_followers = 0
    total_unfollowers = 0

    def __init__(self):
        logging.getLogger('requests').setLevel(logging.WARNING)
        logging.basicConfig(level=logging.DEBUG)

    def check_partnered(self, username):
        user = User()
        req = user.get_channel(username, fields='partnered')
        partnered = req['partnered']

        return partnered

    def connect(self, username):
        print("Connecting to the live-socket")

        ws = create_connection('wss://realtime.beam.pro/socket.io/?EIO=3&transport=websocket')
        self.packet_recv = ws.recv()
        status = str(self.packet_recv.split()[0][0])

        is_partnered = self.check_partnered(username)

        if status == "0":
            # Subscribing to channel events
            self.packet_send = '42' + str(self.pid) + '["put",{"method":"put","headers":{},"data":{"slug":["channel:17887:update"]},"url":"/api/v1/live"}]'
            ws.send(self.packet_send)

            # Subscribing to user events
            self.packet_send = '42' + str(self.pid) + '["put",{"method":"put","headers":{},"data":{"slug":["user:20621:update"]},"url":"/api/v1/live"}]'
            ws.send(self.packet_send)

            # Subscribe to follows
            self.packet_send = '42' + str(self.pid) + '["put",{"method":"put","headers":{},"data":{"slug":["channel:17887:followed"]},"url":"/api/v1/live"}]'
            ws.send(self.packet_send)

            self.pid += 1
            self.packet_recv = ws.recv()
            status = str(self.packet_recv.split()[0][:2])
        else:
            raise Exception("Something terrible happened!")

        if status == "40":
            ws.send("2")
            self.packet_recv = ws.recv()
            status = str(self.packet_recv.split()[0][:2])
        else:
            raise Exception("Something bad went wrong")

        if status == "42":
            print("Connected to the live-socket")

            while True:
                try:
                    recv = str(ws.recv())
                    print(recv)

                    if "viewersCurrent" in recv:
                        self.total_index += 1
                        recv = recv[2:]
                        data = loads(recv)
                        curr = data[1]['viewersCurrent']
                        self.total_viewer += curr
                    elif "viewersTotal" in recv:
                        recv = recv[2:]
                        data = loads(recv)
                        curr = data[1]['viewersTotal']

                        self.total_viewed = curr
                    elif "followed" in recv:
                        recv = recv[2:]
                        data = loads(recv)
                        is_following = (data[1]['following'])

                        if is_following is True:
                            self.total_followers += 1
                        else:
                            self.total_unfollowers += 1
                except:
                    average = self.total_viewer / self.total_index

                    with open('data/stats.json', 'r+') as f:
                        stats = load(f)
                        
                        stats['average-viewers'] = average
                        stats['total-views'] = curr

                        curr_followers = stats['total-followers']
                        stats['total-followers'] = (self.total_followers + int(curr_followers))

                        curr_unfollows = stats['total-unfollows']
                        stats['total-unfolows'] = (self.total_unfollows + int(curr_unfollows))

                        dump(stats, f, indent=4, sort_keys=True)

                    exit()
        else:
            raise Exception("Oh noes! Something went boom!")

server = Server()

server.connect('innectic')
